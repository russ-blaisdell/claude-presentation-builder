#!/usr/bin/env python3
"""Brand Onboarding Wizard — Browser-based brand setup tool.

Runs a local Flask server at http://localhost:5002 with a visual wizard for:
  1. Upload a PPTX template or corpus
  2. View extracted images as thumbnails
  3. Assign images to roles (title, agenda, section, closing, logo)
  4. Preview extracted theme (colors + fonts)
  5. Configure brand name and settings
  6. Build and preview a sample deck

Usage:
    python3 onboard_wizard.py
    python3 onboard_wizard.py --port 5002
"""

import argparse
import base64
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

from flask import Flask, request, jsonify, send_file, send_from_directory

# Ensure we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract_brand_images import extract_all_images
from patch_template_theme import extract_theme, derive_theme, inject_theme, save_theme
from onboard_brand import (
    theme_to_brand_yaml, generate_backgrounds, save_brand_images,
    extract_canvas_size, extract_corpus_colors
)

import yaml
from pptx import Presentation

app = Flask(__name__)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Session state (single-user local tool)
# Can be pre-loaded from CLI via ONBOARD_STATE_FILE env var
_state = {
    'template_path': None,
    'corpus_dir': None,
    'extracted': None,
    'icon_groups': [],
    'theme': None,
    'canvas': None,
    'brand_name': '',
    'selections': {},
}


# ---------------------------------------------------------------------------
# HTML — embedded single-page app
# ---------------------------------------------------------------------------

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brand Onboarding Wizard</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; }

.header { background: #1a1a2e; color: white; padding: 20px 40px; }
.header h1 { font-size: 24px; font-weight: 600; }
.header p { color: #a0a0b0; margin-top: 4px; }

.container { max-width: 1200px; margin: 0 auto; padding: 20px 40px; }

.steps { display: flex; gap: 8px; margin: 20px 0; }
.step { padding: 8px 16px; background: #e0e0e0; border-radius: 20px; font-size: 13px; cursor: pointer; }
.step.active { background: #4a90d9; color: white; }
.step.done { background: #4caf50; color: white; }

.panel { background: white; border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.panel h2 { font-size: 18px; margin-bottom: 16px; }

.upload-zone { border: 2px dashed #ccc; border-radius: 8px; padding: 40px; text-align: center; cursor: pointer; transition: border-color 0.2s; }
.upload-zone:hover { border-color: #4a90d9; }
.upload-zone.dragging { border-color: #4a90d9; background: #f0f7ff; }
.upload-zone input { display: none; }

.image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.image-card { border: 2px solid #e0e0e0; border-radius: 8px; overflow: hidden; cursor: pointer; transition: border-color 0.2s, transform 0.1s; }
.image-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
.image-card.selected { border-color: #4a90d9; }

/* Slide-shaped frame: 16:9 outline with checkerboard to show uncovered areas */
.slide-frame { position: relative; width: 100%; padding-bottom: 56.25%; border: 1px solid #ccc; overflow: hidden;
    background-image: linear-gradient(45deg, #d0d0d0 25%, transparent 25%),
        linear-gradient(-45deg, #d0d0d0 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #d0d0d0 75%),
        linear-gradient(-45deg, transparent 75%, #d0d0d0 75%);
    background-size: 12px 12px;
    background-position: 0 0, 0 6px, 6px -6px, -6px 0;
    background-color: #e8e8e8; }
/* Placement wrapper: represents where PPTX places the image on the slide.
   White background so transparent PNGs render on white (like PowerPoint),
   while the checkerboard frame shows through only in uncovered areas. */
.slide-frame .img-placement { position: absolute; overflow: hidden; background: white; }
/* Image fills its placement area, cropping to fit (like PowerPoint) */
.slide-frame .img-placement img { width: 100%; height: 100%; object-fit: cover; }

.image-card .meta { padding: 8px; font-size: 12px; color: #666; }
.image-card .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; color: white; margin-right: 3px; }
.badge-title { background: #4a90d9; }
.badge-agenda { background: #9c27b0; }
.badge-section { background: #ff9800; }
.badge-closing { background: #607d8b; }
.badge-logo { background: #e91e63; }

/* Full-size preview overlay on hover */
.preview-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center; }
.preview-overlay.active { display: flex; }
.preview-slide { position: relative; width: 80vw; max-width: 960px; border: 2px solid white; border-radius: 4px;
    background-image: linear-gradient(45deg, #d0d0d0 25%, transparent 25%),
        linear-gradient(-45deg, #d0d0d0 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #d0d0d0 75%),
        linear-gradient(-45deg, transparent 75%, #d0d0d0 75%);
    background-size: 16px 16px;
    background-position: 0 0, 0 8px, 8px -8px, -8px 0;
    background-color: #e8e8e8; }
.preview-slide::before { content: ''; display: block; padding-bottom: 56.25%; }
.preview-slide .img-placement { position: absolute; overflow: hidden; background: white; }
.preview-slide .img-placement img { width: 100%; height: 100%; object-fit: cover; }
.preview-label { position: absolute; bottom: -30px; left: 0; right: 0; text-align: center; color: white; font-size: 14px; }

.role-buttons { display: flex; gap: 6px; padding: 6px 8px; flex-wrap: wrap; }
.role-btn { padding: 4px 10px; border: 1px solid #ddd; border-radius: 12px; font-size: 11px; cursor: pointer; background: white; transition: all 0.15s; }
.role-btn:hover { background: #f0f0f0; }
.role-btn.active { color: white; border-color: transparent; }
.role-btn[data-role="title"].active { background: #4a90d9; }
.role-btn[data-role="agenda"].active { background: #9c27b0; }
.role-btn[data-role="section"].active { background: #ff9800; }
.role-btn[data-role="closing"].active { background: #607d8b; }
.role-btn[data-role="logo"].active { background: #e91e63; }

.theme-preview { display: flex; gap: 24px; flex-wrap: wrap; }
.color-grid { display: flex; gap: 8px; flex-wrap: wrap; }
.color-swatch { width: 60px; height: 40px; border-radius: 6px; border: 1px solid #ddd; position: relative; }
.color-swatch span { position: absolute; bottom: -18px; left: 0; right: 0; text-align: center; font-size: 10px; color: #666; }
.font-preview { font-size: 20px; padding: 8px 16px; background: #f9f9f9; border-radius: 6px; }

.brand-input { display: flex; gap: 12px; align-items: center; margin: 12px 0; }
.brand-input input { padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; width: 300px; }
.brand-input label { font-weight: 600; }

.btn { padding: 10px 24px; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; font-weight: 600; transition: opacity 0.2s; }
.btn:hover { opacity: 0.9; }
.btn-primary { background: #4a90d9; color: white; }
.btn-success { background: #4caf50; color: white; }
.btn-lg { padding: 14px 32px; font-size: 16px; }

.actions { display: flex; gap: 12px; margin: 20px 0; }

.summary-table { width: 100%; border-collapse: collapse; }
.summary-table td, .summary-table th { padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }
.summary-table th { font-weight: 600; color: #666; }

.status { padding: 12px 16px; border-radius: 6px; margin: 12px 0; }
.status-success { background: #e8f5e9; color: #2e7d32; }
.status-error { background: #fde8e8; color: #c62828; }
.status-info { background: #e3f2fd; color: #1565c0; }

.hidden { display: none; }

.icon-card { border: 2px solid #e0e0e0; border-radius: 8px; padding: 8px; text-align: center; transition: all 0.15s; }
.icon-card.selected { border-color: #4a90d9; background: #f8fbff; }
.icon-card.deselected { border-color: #eee; opacity: 0.4; }
.icon-card img { width: 48px; height: 48px; object-fit: contain; margin: 4px auto; display: block; }
.icon-card input { width: 100%; border: 1px solid #ddd; border-radius: 4px; padding: 3px 6px; font-size: 11px; text-align: center; margin-top: 4px; }
.icon-card .icon-toggle { cursor: pointer; font-size: 11px; color: #999; margin-top: 2px; }
.icon-card .icon-cat { font-size: 10px; color: #888; }
.loading { opacity: 0.5; pointer-events: none; }
</style>
</head>
<body>

<div class="header">
    <h1>Brand Onboarding Wizard</h1>
    <p>Extract theme and images from your company's PPTX template</p>
</div>

<div class="container">
    <div class="steps">
        <div class="step active" data-step="1">1. Upload</div>
        <div class="step" data-step="2">2. Images</div>
        <div class="step" data-step="3">3. Theme</div>
        <div class="step" data-step="4">4. Finalize</div>
    </div>

    <!-- STEP 1: Upload -->
    <div id="step1" class="panel">
        <h2>Upload Template</h2>
        <p style="margin-bottom:16px; color:#666;">Upload your company's PPTX template file. We'll extract the theme, images, and logo.</p>

        <div class="brand-input">
            <label>Brand Name:</label>
            <input type="text" id="brandName" placeholder="e.g. acme-corp" oninput="validateBrandName()" />
            <span id="brandNameStatus" style="font-size:13px;"></span>
        </div>

        <div class="upload-zone" id="uploadZone">
            <p style="font-size:18px; margin-bottom:8px;">Drop PPTX file here or click to browse</p>
            <p style="color:#999;">Supports .pptx template files</p>
            <input type="file" id="fileInput" accept=".pptx" />
        </div>

        <div id="uploadStatus" class="status status-info hidden"></div>
    </div>

    <!-- STEP 2: Images -->
    <div id="step2" class="panel hidden">
        <h2>Assign Images to Roles</h2>
        <p style="margin-bottom:16px; color:#666;">Click role buttons under each image to assign it. An image can have multiple roles. <strong>Images without a role assigned will be ignored.</strong></p>

        <div id="imageCategories"></div>

        <div id="iconSection" class="hidden" style="margin-top: 24px; border-top: 2px solid #eee; padding-top: 20px;">
            <h2>Icons</h2>
            <p style="margin-bottom:12px; color:#666;">
                Extracted icons are pre-selected. Uncheck any you don't want. Edit labels by clicking the name.
                <button class="btn" style="padding:4px 12px; font-size:12px; margin-left:8px;" onclick="labelIconsAI()">Auto-label with AI</button>
            </p>
            <div id="iconGrid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px;"></div>
        </div>
    </div>

    <!-- STEP 3: Theme -->
    <div id="step3" class="panel hidden">
        <h2>Theme Preview</h2>
        <p style="margin-bottom:16px; color:#666;">Extracted from your template's theme. These colors and fonts will be used for all decks.</p>

        <div class="theme-preview">
            <div>
                <h3 style="margin-bottom:8px;">Colors</h3>
                <div id="colorGrid" class="color-grid"></div>
            </div>
            <div>
                <h3 style="margin-bottom:8px;">Fonts</h3>
                <div id="fontPreview"></div>
            </div>
        </div>
    </div>

    <!-- STEP 4: Finalize -->
    <div id="step4" class="panel hidden">
        <h2>Brand Package Summary</h2>

        <div id="summary"></div>

        <div class="actions" style="margin-top:24px;">
            <button class="btn btn-success btn-lg" onclick="finalize()">Create Brand Package</button>
        </div>

        <div id="finalStatus" class="hidden"></div>
    </div>

    <div class="actions">
        <button class="btn btn-primary" id="prevBtn" onclick="prevStep()" style="display:none;">Previous</button>
        <button class="btn btn-primary" id="nextBtn" onclick="nextStep()" style="display:none;">Next</button>
    </div>
</div>

<script>
let currentStep = 1;
let state = { images: [], icons: [], theme: null, selections: {} };

// Check for pre-loaded state from CLI
(async function checkPreloaded() {
    try {
        const resp = await fetch('/api/preloaded');
        const data = await resp.json();
        if (data.preloaded) {
            state.images = data.images || [];
            state.icons = data.icons || [];
            state.theme = data.theme || {};
            state.brandNameValid = true;
            state.brandSlug = data.brand_name;
            document.getElementById('brandName').value = data.brand_name;
            document.getElementById('brandNameStatus').innerHTML =
                `<span style="color:#2e7d32;">\u2713 pre-loaded from CLI</span>`;
            document.getElementById('uploadStatus').classList.remove('hidden');
            document.getElementById('uploadStatus').className = 'status status-success';
            const iconMsg = state.icons.length ? `, ${state.icons.length} icons` : '';
            document.getElementById('uploadStatus').textContent =
                `Pre-loaded: ${state.images.length} images${iconMsg}, theme extracted. Click Next to review.`;
            renderImages();
            renderIcons();
            document.getElementById('nextBtn').style.display = '';
        }
    } catch (e) { /* no preloaded state, normal flow */ }
})();

// --- Navigation ---
function showStep(n) {
    for (let i = 1; i <= 4; i++) {
        document.getElementById('step' + i).classList.toggle('hidden', i !== n);
        const stepEl = document.querySelector('.step[data-step="' + i + '"]');
        stepEl.classList.toggle('active', i === n);
        stepEl.classList.toggle('done', i < n);
    }
    currentStep = n;
    document.getElementById('prevBtn').style.display = n > 1 ? '' : 'none';
    document.getElementById('nextBtn').style.display = n < 4 ? '' : 'none';
}

function nextStep() {
    if (currentStep === 1) {
        if (!state.brandNameValid) { alert('Please enter a valid brand name.'); return; }
        if (!state.theme) { alert('Please upload a template first.'); return; }
    }
    showStep(Math.min(currentStep + 1, 4));
    if (currentStep === 3) renderTheme();
    if (currentStep === 4) renderSummary();
}

// --- Brand name validation ---
let _nameTimer = null;
state.brandNameValid = false;
state.brandSlug = '';

function validateBrandName() {
    const input = document.getElementById('brandName');
    const status = document.getElementById('brandNameStatus');
    const name = input.value.trim();

    if (!name) {
        status.innerHTML = '';
        state.brandNameValid = false;
        return;
    }

    // Debounce
    clearTimeout(_nameTimer);
    status.innerHTML = '<span style="color:#999;">checking...</span>';
    _nameTimer = setTimeout(async () => {
        try {
            const resp = await fetch('/api/validate-name?name=' + encodeURIComponent(name));
            const data = await resp.json();
            if (!data.valid) {
                status.innerHTML = `<span style="color:#c62828;">\u2717 ${data.error}</span>`;
                state.brandNameValid = false;
            } else if (data.exists) {
                status.innerHTML = `<span style="color:#e65100;">\u26A0 "${data.slug}" exists \u2014 will overwrite</span>`;
                state.brandNameValid = true;
                state.brandSlug = data.slug;
            } else {
                status.innerHTML = `<span style="color:#2e7d32;">\u2713 "${data.slug}" available</span>`;
                state.brandNameValid = true;
                state.brandSlug = data.slug;
            }
        } catch (err) {
            status.innerHTML = `<span style="color:#c62828;">Error: ${err.message}</span>`;
        }
    }, 300);
}

function prevStep() { showStep(Math.max(currentStep - 1, 1)); }

// --- Upload ---
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');

uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragging'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragging'));
uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    uploadZone.classList.remove('dragging');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files.length) handleFile(fileInput.files[0]); });

async function handleFile(file) {
    if (!file.name.endsWith('.pptx')) { alert('Please upload a .pptx file'); return; }

    const statusEl = document.getElementById('uploadStatus');
    statusEl.classList.remove('hidden');
    statusEl.className = 'status status-info';
    statusEl.textContent = 'Uploading and analyzing template...';

    const formData = new FormData();
    formData.append('template', file);
    formData.append('brand_name', state.brandSlug || document.getElementById('brandName').value || 'new-brand');

    try {
        const resp = await fetch('/api/upload', { method: 'POST', body: formData });
        const data = await resp.json();

        if (data.error) {
            statusEl.className = 'status status-error';
            statusEl.textContent = 'Error: ' + data.error;
            return;
        }

        state.images = data.images || [];
        state.icons = data.icons || [];
        state.theme = data.theme || {};
        statusEl.className = 'status status-success';
        const iconMsg = state.icons.length ? `, ${state.icons.length} icons` : '';
        statusEl.textContent = `Extracted ${state.images.length} images${iconMsg}, theme with ${Object.keys(state.theme.colors || {}).length} colors.`;

        renderImages();
        renderIcons();
        document.getElementById('nextBtn').style.display = '';
    } catch (err) {
        statusEl.className = 'status status-error';
        statusEl.textContent = 'Upload failed: ' + err.message;
    }
}

// --- Images ---
// Slide dimensions for scaling (10" x 5.625")
const SLIDE_W = 10.0;
const SLIDE_H = 5.625;

function renderImages() {
    const container = document.getElementById('imageCategories');
    const categories = {
        'full-bleed': { label: 'Backgrounds (full-slide images)', roles: ['title', 'section', 'closing'] },
        'panel': { label: 'Panels (agenda side images)', roles: ['agenda'] },
        'logo': { label: 'Logos', roles: ['logo'] },
        'other': { label: 'Other Images', roles: ['title', 'agenda', 'section', 'closing'] },
    };

    let html = '';
    for (const [cat, info] of Object.entries(categories)) {
        const imgs = state.images.filter(img => img.category === cat);
        if (!imgs.length) continue;

        const selectedCount = imgs.filter(img => (state.selections[img.hash] || []).length > 0).length;
        const selLabel = selectedCount > 0
            ? `<span style="color:#4caf50; font-weight:600;">${selectedCount} selected</span>`
            : `<span style="color:#999;">0 selected</span>`;
        html += `<h3 style="margin: 20px 0 10px;">${info.label} (${imgs.length} images, ${selLabel})</h3>`;
        html += '<div class="image-grid">';
        for (const img of imgs) {
            const roles = state.selections[img.hash] || [];
            const badges = roles.map(r => `<span class="badge badge-${r}">${r}</span>`).join(' ');

            // Calculate image position within slide frame (percentage-based)
            const imgWPct = Math.min(100, (img.width / SLIDE_W) * 100);
            const imgHPct = Math.min(100, (img.height / SLIDE_H) * 100);
            // Center the image in the frame
            const leftPct = (100 - imgWPct) / 2;
            const topPct = (100 - imgHPct) / 2;

            html += `<div class="image-card ${roles.length ? 'selected' : ''}" id="card-${img.hash}">`;
            html += `<div class="slide-frame" onclick="showPreview('${img.hash}', ${img.width}, ${img.height})">`;
            html += `<div class="img-placement" style="left:${leftPct}%;top:${topPct}%;width:${imgWPct}%;height:${imgHPct}%;">`;
            html += `<img src="/api/image/${img.hash}" alt="${cat}" />`;
            html += `</div></div>`;
            html += `<div class="meta">${img.width}"x${img.height}" &middot; ${img.size_kb}KB ${badges}</div>`;
            html += '<div class="role-buttons">';
            for (const role of info.roles) {
                const active = roles.includes(role) ? 'active' : '';
                html += `<button class="role-btn ${active}" data-role="${role}" onclick="event.stopPropagation(); toggleRole('${img.hash}','${role}')">${role}</button>`;
            }
            html += '</div></div>';
        }
        html += '</div>';
    }

    // Add preview overlay (hidden by default)
    html += `<div class="preview-overlay" id="previewOverlay" onclick="hidePreview()">
        <div>
            <div class="preview-slide" id="previewSlide"></div>
            <div class="preview-label" id="previewLabel"></div>
        </div>
    </div>`;

    container.innerHTML = html;
}

function showPreview(hash, imgW, imgH) {
    const overlay = document.getElementById('previewOverlay');
    const slide = document.getElementById('previewSlide');
    const label = document.getElementById('previewLabel');

    const wPct = Math.min(100, (imgW / SLIDE_W) * 100);
    const hPct = Math.min(100, (imgH / SLIDE_H) * 100);
    const leftPct = (100 - wPct) / 2;
    const topPct = (100 - hPct) / 2;

    slide.innerHTML = `<div class="img-placement" style="left:${leftPct}%;top:${topPct}%;width:${wPct}%;height:${hPct}%;"><img src="/api/image/${hash}" /></div>`;
    label.textContent = `${imgW}" x ${imgH}" — shown at actual slide scale (10" x 5.625")`;
    overlay.classList.add('active');
}

function hidePreview() {
    document.getElementById('previewOverlay').classList.remove('active');
}

function toggleRole(hash, role) {
    if (!state.selections[hash]) state.selections[hash] = [];
    const arr = state.selections[hash];
    const idx = arr.indexOf(role);
    if (idx >= 0) arr.splice(idx, 1);
    else arr.push(role);
    renderImages();
}

// --- Icons ---
function renderIcons() {
    const section = document.getElementById('iconSection');
    const grid = document.getElementById('iconGrid');
    if (!state.icons || !state.icons.length) {
        section.classList.add('hidden');
        return;
    }
    section.classList.remove('hidden');

    const selectedCount = state.icons.filter(ic => ic.selected).length;
    const heading = section.querySelector('h2');
    heading.textContent = `Icons (${state.icons.length} found, ${selectedCount} selected)`;

    let html = '';
    for (const icon of state.icons) {
        const cls = icon.selected ? 'selected' : 'deselected';
        html += `<div class="icon-card ${cls}" id="icon-${icon.group_idx}">`;
        html += `<img src="/api/icon/${icon.group_idx}" alt="${icon.name}" />`;
        html += `<input type="text" value="${icon.name}" onchange="renameIcon(${icon.group_idx}, this.value)" />`;
        html += `<div class="icon-cat">${icon.category} · ${icon.variants}v</div>`;
        html += `<div class="icon-toggle" onclick="toggleIcon(${icon.group_idx})">${icon.selected ? '✓ included' : '✗ excluded'}</div>`;
        html += '</div>';
    }
    grid.innerHTML = html;
}

function toggleIcon(idx) {
    const icon = state.icons.find(ic => ic.group_idx === idx);
    if (icon) {
        icon.selected = !icon.selected;
        renderIcons();
    }
}

function renameIcon(idx, newName) {
    const icon = state.icons.find(ic => ic.group_idx === idx);
    if (icon) icon.name = newName;
}

async function labelIconsAI() {
    const btn = event.target;
    btn.textContent = 'Labeling...';
    btn.disabled = true;
    try {
        const resp = await fetch('/api/label-icons', { method: 'POST' });
        const data = await resp.json();
        if (data.labels) {
            for (const label of data.labels) {
                const icon = state.icons.find(ic => ic.group_idx === label.group_idx);
                if (icon) {
                    icon.name = label.name;
                    icon.category = label.category;
                }
            }
            renderIcons();
            btn.textContent = 'Labels updated!';
        } else {
            btn.textContent = 'Labeling failed';
        }
    } catch (err) {
        btn.textContent = 'Error: ' + err.message;
    }
    setTimeout(() => { btn.textContent = 'Auto-label with AI'; btn.disabled = false; }, 3000);
}

// --- Theme ---
function renderTheme() {
    const colors = state.theme.colors || {};
    const fonts = state.theme.fonts || {};

    const colorLabels = {
        dk1: 'Headlines', dk2: 'Secondary', lt1: 'Light', lt2: 'Light BG',
        accent1: 'Accent 1', accent2: 'Accent 2', accent3: 'Accent 3', accent4: 'Accent 4',
        accent5: 'Accent 5', accent6: 'Accent 6', hlink: 'Link', folHlink: 'Visited',
    };

    let colorHtml = '';
    for (const [slot, label] of Object.entries(colorLabels)) {
        const color = colors[slot] || '#ccc';
        colorHtml += `<div style="text-align:center; margin-bottom:20px;">
            <div class="color-swatch" style="background:${color};"></div>
            <span>${label}<br/>${color}</span>
        </div>`;
    }
    document.getElementById('colorGrid').innerHTML = colorHtml;

    document.getElementById('fontPreview').innerHTML = `
        <div class="font-preview" style="font-family:'${fonts.heading}',sans-serif; font-weight:800;">
            ${fonts.heading || 'Arial'} (Headings)
        </div>
        <div class="font-preview" style="font-family:'${fonts.body}',sans-serif; margin-top:8px;">
            ${fonts.body || 'Arial'} (Body text)
        </div>
    `;
}

// --- Summary ---
function renderSummary() {
    const name = document.getElementById('brandName').value || 'new-brand';
    const roleCount = {};
    for (const roles of Object.values(state.selections)) {
        for (const r of roles) roleCount[r] = (roleCount[r] || 0) + 1;
    }

    let html = '<table class="summary-table">';
    html += '<tr><th>Setting</th><th>Value</th></tr>';
    html += `<tr><td>Brand Name</td><td><strong>${name}</strong></td></tr>`;
    html += `<tr><td>Heading Font</td><td>${state.theme.fonts?.heading || 'Arial'}</td></tr>`;
    html += `<tr><td>Body Font</td><td>${state.theme.fonts?.body || 'Arial'}</td></tr>`;
    html += `<tr><td>Primary Color (dk1)</td><td><span style="background:${state.theme.colors?.dk1};color:white;padding:2px 8px;border-radius:4px;">${state.theme.colors?.dk1}</span></td></tr>`;
    html += `<tr><td>Title Backgrounds</td><td>${roleCount.title || 0} images</td></tr>`;
    html += `<tr><td>Agenda Panels</td><td>${roleCount.agenda || 0} images</td></tr>`;
    html += `<tr><td>Section Dividers</td><td>${roleCount.section || 0} images</td></tr>`;
    html += `<tr><td>Closing Backgrounds</td><td>${roleCount.closing || 0} images</td></tr>`;
    html += `<tr><td>Logo</td><td>${roleCount.logo || 0} found</td></tr>`;
    html += '</table>';

    document.getElementById('summary').innerHTML = html;
}

// --- Finalize ---
async function finalize() {
    const name = state.brandSlug || document.getElementById('brandName').value || 'new-brand';
    const statusEl = document.getElementById('finalStatus');
    statusEl.classList.remove('hidden');
    statusEl.className = 'status status-info';
    statusEl.textContent = 'Creating brand package...';

    try {
        const resp = await fetch('/api/finalize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ brand_name: name, selections: state.selections }),
        });
        const data = await resp.json();
        if (data.error) {
            statusEl.className = 'status status-error';
            statusEl.textContent = 'Error: ' + data.error;
        } else {
            statusEl.className = 'status status-success';
            statusEl.innerHTML = `Brand package created at: <strong>${data.output_dir}</strong><br/>
                Files: brand.yaml, theme.json, template.pptx, title-assets/<br/>
                Use: <code>brand: ${name}</code> in your YAML deck definition`;
        }
    } catch (err) {
        statusEl.className = 'status status-error';
        statusEl.textContent = 'Error: ' + err.message;
    }
}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return HTML_PAGE


@app.route('/api/upload', methods=['POST'])
def upload_template():
    """Handle template upload — extract theme and images."""
    if 'template' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['template']
    brand_name = request.form.get('brand_name', 'new-brand')

    # Save to temp location
    tmp_dir = tempfile.mkdtemp(prefix='onboard-')
    tmp_path = os.path.join(tmp_dir, file.filename)
    file.save(tmp_path)

    try:
        # Extract theme
        theme = extract_theme(tmp_path)
        prs = Presentation(tmp_path)
        canvas = extract_canvas_size(prs)

        # Extract images
        extracted = extract_all_images(tmp_path)

        # Prepare image data for frontend (without blobs, add base64 thumbnails)
        images = []
        for img in extracted['images']:
            if img['category'] in ('icon', 'small'):
                continue
            images.append({
                'hash': img['hash'],
                'category': img['category'],
                'content_type': img['content_type'],
                'size_kb': img['size_kb'],
                'width': img['width'],
                'height': img['height'],
                'num_slides': img['num_slides'],
                'slides': img['slides'],
            })

        # Extract icons
        from extract_icons import extract_icons_from_pptx, deduplicate_icons
        raw_icons = extract_icons_from_pptx(tmp_path)
        icon_groups = deduplicate_icons(raw_icons)
        icon_data = []
        for i, group in enumerate(icon_groups):
            rep = group[0]
            icon_data.append({
                'group_idx': i,
                'hash': rep['hash'],
                'variants': len(group),
                'name': f'icon-{i+1:03d}',
                'category': 'other',
                'selected': True,
            })

        # Store state for later use
        _state['template_path'] = tmp_path
        _state['extracted'] = extracted
        _state['icon_groups'] = icon_groups
        _state['theme'] = theme
        _state['canvas'] = canvas
        _state['brand_name'] = brand_name

        return jsonify({
            'theme': theme,
            'canvas': canvas,
            'images': images,
            'icons': icon_data,
            'icon_count': len(icon_groups),
            'stats': extracted['stats'],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/image/<img_hash>')
def serve_image(img_hash):
    """Serve an extracted image by its hash."""
    if not _state['extracted']:
        return 'No images extracted', 404

    for img in _state['extracted']['images']:
        if img['hash'] == img_hash:
            mime = img['content_type']
            return send_file(io.BytesIO(img['blob']), mimetype=mime)

    return 'Image not found', 404


@app.route('/api/icon/<int:group_idx>')
def serve_icon(group_idx):
    """Serve an icon by its group index."""
    groups = _state.get('icon_groups', [])
    if group_idx < 0 or group_idx >= len(groups):
        return 'Icon not found', 404
    rep = groups[group_idx][0]
    return send_file(io.BytesIO(rep['blob']), mimetype=rep['content_type'])


@app.route('/api/label-icons', methods=['POST'])
def label_icons():
    """AI-label icons using Claude Code CLI (parallel batches)."""
    groups = _state.get('icon_groups', [])
    if not groups:
        return jsonify({'error': 'No icons extracted'}), 400

    from extract_icons import label_icons_with_claude_code
    try:
        labels = label_icons_with_claude_code(groups)
        return jsonify({'labels': labels})
    except Exception as e:
        # Fall back to generic labels
        from extract_icons import _generic_labels
        labels = _generic_labels(groups)
        return jsonify({'labels': labels, 'warning': str(e)})


@app.route('/api/validate-name')
def validate_brand_name():
    """Check if a brand name is valid and available."""
    import re
    name = request.args.get('name', '').strip()

    if not name:
        return jsonify({'valid': False, 'error': 'Name is required'})

    # Sanitize: lowercase, replace spaces with hyphens
    slug = re.sub(r'[^a-z0-9-]', '', name.lower().replace(' ', '-'))
    slug = re.sub(r'-+', '-', slug).strip('-')

    if not slug:
        return jsonify({'valid': False, 'error': 'Name must contain letters or numbers'})

    if len(slug) < 2:
        return jsonify({'valid': False, 'error': 'Name too short (min 2 characters)'})

    if len(slug) > 40:
        return jsonify({'valid': False, 'error': 'Name too long (max 40 characters)'})

    brand_dir = os.path.join(SCRIPT_DIR, 'brands', slug)
    exists = os.path.isdir(brand_dir)

    return jsonify({
        'valid': True,
        'slug': slug,
        'exists': exists,
        'warning': f'Brand "{slug}" already exists — will be overwritten' if exists else None,
    })


@app.route('/api/finalize', methods=['POST'])
def finalize_brand():
    """Create the brand package from selections."""
    data = request.json
    brand_name = data.get('brand_name', 'new-brand')
    selections_map = data.get('selections', {})  # hash -> [roles]

    if not _state['theme']:
        return jsonify({'error': 'No template uploaded yet'}), 400

    output_dir = os.path.join(SCRIPT_DIR, 'brands', brand_name)
    os.makedirs(output_dir, exist_ok=True)

    theme = _state['theme']
    canvas = _state['canvas']
    extracted = _state['extracted']

    # Save theme
    save_theme(theme, os.path.join(output_dir, 'theme.json'))

    # Copy template
    if _state['template_path']:
        shutil.copy2(_state['template_path'], os.path.join(output_dir, 'template.pptx'))

    # Process image selections into role-based lists
    role_images = {'title': [], 'agenda': [], 'section': [], 'closing': [], 'logo': None}

    for img in extracted['images']:
        roles = selections_map.get(img['hash'], [])
        for role in roles:
            if role == 'logo':
                role_images['logo'] = img
            elif role in role_images:
                role_images[role].append(img)

    # Save images
    image_paths = save_brand_images(role_images, output_dir)

    # Generate gradient backgrounds if no title images selected
    if not role_images['title']:
        primary = theme['colors'].get('dk1', '#1A365D')
        secondary = theme['colors'].get('dk2', '#3182CE')
        generate_backgrounds(output_dir, primary, secondary)
        image_paths['title_backgrounds'] = {"default": "title-assets/title-bg.jpg"}
        image_paths['agenda_backgrounds'] = image_paths.get('agenda_backgrounds') or {"default": "title-assets/agenda-left.jpg"}

    # Generate brand.yaml
    brand_data = theme_to_brand_yaml(brand_name, theme, canvas,
                                     image_paths=image_paths)
    with open(os.path.join(output_dir, 'brand.yaml'), 'w') as f:
        yaml.dump(brand_data, f, default_flow_style=False, sort_keys=False)

    # Inject theme into template
    template_out = os.path.join(output_dir, 'template.pptx')
    if os.path.isfile(template_out):
        inject_theme(template_out, theme)

    # Extract and save layout mapping
    if os.path.isfile(template_out):
        from extract_layout_mapping import extract_layout_mapping
        mapping = extract_layout_mapping(template_out)
        clean_mapping = {k: v for k, v in mapping.items() if k != 'all_placeholders'}
        with open(os.path.join(output_dir, 'layout_mapping.json'), 'w') as f:
            json.dump(clean_mapping, f, indent=2)

    return jsonify({
        'success': True,
        'output_dir': output_dir,
        'brand_name': brand_name,
    })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _load_preextracted_state():
    """Load pre-extracted state from CLI if ONBOARD_STATE_FILE is set."""
    state_file = os.environ.get('ONBOARD_STATE_FILE')
    if not state_file or not os.path.isfile(state_file):
        return

    import json as _json
    with open(state_file) as f:
        pre = _json.load(f)

    template_path = pre.get('template_path')
    if template_path and os.path.isfile(template_path):
        _state['template_path'] = template_path
        _state['theme'] = pre.get('theme')
        _state['canvas'] = pre.get('canvas')
        _state['brand_name'] = pre.get('brand_name', '')

        # Re-extract images and icons (need blobs for serving)
        extracted = extract_all_images(template_path)
        _state['extracted'] = extracted

        from extract_icons import extract_icons_from_pptx, deduplicate_icons
        raw_icons = extract_icons_from_pptx(template_path)
        _state['icon_groups'] = deduplicate_icons(raw_icons)

        # Apply pre-computed AI labels if available
        _state['_precomputed_labels'] = pre.get('icon_labels', [])

        print(f"  Pre-loaded state for brand: {_state['brand_name']}")
        print(f"  {len(extracted['images'])} images, {len(_state['icon_groups'])} icon groups")


@app.route('/api/preloaded')
def get_preloaded():
    """Return pre-extracted state if available (from CLI launch)."""
    if not _state.get('theme'):
        return jsonify({'preloaded': False})

    images = []
    if _state.get('extracted'):
        for img in _state['extracted']['images']:
            if img['category'] in ('icon', 'small'):
                continue
            images.append({
                'hash': img['hash'],
                'category': img['category'],
                'content_type': img['content_type'],
                'size_kb': img['size_kb'],
                'width': img['width'],
                'height': img['height'],
                'num_slides': img['num_slides'],
                'slides': img['slides'],
            })

    icon_data = []
    pre_labels = _state.get('_precomputed_labels', [])
    for i, group in enumerate(_state.get('icon_groups', [])):
        rep = group[0]
        label = pre_labels[i] if i < len(pre_labels) else {}
        icon_data.append({
            'group_idx': i,
            'hash': rep['hash'],
            'variants': len(group),
            'name': label.get('name', f'icon-{i+1:03d}'),
            'category': label.get('category', 'other'),
            'selected': True,
        })

    return jsonify({
        'preloaded': True,
        'brand_name': _state.get('brand_name', ''),
        'theme': _state['theme'],
        'canvas': _state.get('canvas'),
        'images': images,
        'icons': icon_data,
    })


def main():
    parser = argparse.ArgumentParser(description="Brand Onboarding Wizard")
    parser.add_argument('--port', type=int, default=5002, help='Port (default: 5002)')
    parser.add_argument('--host', default='127.0.0.1', help='Host (default: 127.0.0.1)')
    args = parser.parse_args()

    # Load pre-extracted state from CLI if available
    _load_preextracted_state()

    print(f"\n  Brand Onboarding Wizard")
    print(f"  Open: http://{args.host}:{args.port}")
    print(f"  Press Ctrl+C to stop\n")

    app.run(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    main()
