#!/usr/bin/env bash
#
# Claude Pres Builder — First-Time Setup
#
# Run after cloning:  ./setup.sh
# Re-run after pull:  ./setup.sh  (idempotent — only does what's needed)
#
# What it does:
#   1. Finds Python >= 3.10 and creates .venv/
#   2. Installs dependencies (python-pptx, pyyaml, Pillow)
#   3. Symlinks the /create-presentation skill into ~/.claude/skills/
#   4. Detects optional tools (LibreOffice, gog CLI, Claude Code)
#   5. Optionally creates your company brand from a PPTX template
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
SKILL_SRC="$SCRIPT_DIR/.claude/skills/create-presentation"
SKILL_DST="$HOME/.claude/skills/create-presentation"
MIN_PYTHON="3.10"

# Colors (skip if not a terminal)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    RED='\033[0;31m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    GREEN='' YELLOW='' RED='' BOLD='' NC=''
fi

ok()   { echo -e "${GREEN}[OK]${NC}  $1"; }
warn() { echo -e "${YELLOW}[--]${NC}  $1"; }
fail() { echo -e "${RED}[!!]${NC}  $1"; }
header() { echo -e "\n${BOLD}$1${NC}"; }

# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

version_gte() {
    # Returns 0 if $1 >= $2 (semantic version comparison)
    printf '%s\n%s\n' "$2" "$1" | sort -V | head -n1 | grep -qx "$2"
}

find_python() {
    # Try common Python commands, return first one >= MIN_PYTHON
    for cmd in python3 python python3.14 python3.13 python3.12 python3.11 python3.10; do
        if command -v "$cmd" &>/dev/null; then
            ver=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)
            if [ -n "$ver" ] && version_gte "$ver" "$MIN_PYTHON"; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

find_libreoffice() {
    # Check common LibreOffice locations
    if command -v soffice &>/dev/null; then
        echo "soffice"
        return 0
    elif [ -f "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
        echo "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        return 0
    elif [ -f "/usr/bin/soffice" ]; then
        echo "/usr/bin/soffice"
        return 0
    fi
    # Windows paths (Git Bash / WSL)
    for p in "/c/Program Files/LibreOffice/program/soffice.exe" \
             "/mnt/c/Program Files/LibreOffice/program/soffice.exe"; do
        if [ -f "$p" ]; then
            echo "$p"
            return 0
        fi
    done
    return 1
}

# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

echo ""
echo "======================================"
echo "  Claude Pres Builder — Setup"
echo "======================================"

# ── Step 1: Python ──────────────────────────────────────────────────

header "Python"

PYTHON_CMD=""
if [ -f "$VENV_DIR/bin/python3" ]; then
    PYTHON_CMD="$VENV_DIR/bin/python3"
    ver=$("$PYTHON_CMD" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)
    ok "Python $ver (existing venv)"
elif [ -f "$VENV_DIR/Scripts/python.exe" ]; then
    # Windows venv
    PYTHON_CMD="$VENV_DIR/Scripts/python.exe"
    ver=$("$PYTHON_CMD" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)
    ok "Python $ver (existing venv, Windows)"
else
    SYS_PYTHON=$(find_python) || true
    if [ -z "$SYS_PYTHON" ]; then
        fail "Python >= $MIN_PYTHON not found"
        echo ""
        echo "    Install Python 3.10+ from https://python.org/downloads/"
        echo "    On macOS: brew install python@3.12"
        echo "    On Ubuntu: sudo apt install python3.12"
        echo ""
        exit 1
    fi
    ver=$("$SYS_PYTHON" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)
    ok "Python $ver ($SYS_PYTHON)"

    echo "    Creating virtual environment..."
    "$SYS_PYTHON" -m venv "$VENV_DIR"
    if [ -f "$VENV_DIR/bin/python3" ]; then
        PYTHON_CMD="$VENV_DIR/bin/python3"
    elif [ -f "$VENV_DIR/Scripts/python.exe" ]; then
        PYTHON_CMD="$VENV_DIR/Scripts/python.exe"
    fi
    ok "Virtual environment created (.venv/)"
fi

# ── Step 2: Dependencies ───────────────────────────────────────────

header "Dependencies"

# Determine pip path
if [ -f "$VENV_DIR/bin/pip" ]; then
    PIP="$VENV_DIR/bin/pip"
elif [ -f "$VENV_DIR/Scripts/pip.exe" ]; then
    PIP="$VENV_DIR/Scripts/pip.exe"
else
    fail "pip not found in venv"
    exit 1
fi

# Check if core deps are installed
DEPS_NEEDED=false
for pkg in pptx yaml PIL; do
    if ! "$PYTHON_CMD" -c "import $pkg" 2>/dev/null; then
        DEPS_NEEDED=true
        break
    fi
done

if [ "$DEPS_NEEDED" = true ]; then
    echo "    Installing dependencies..."
    "$PIP" install --quiet python-pptx pyyaml Pillow lxml 2>&1 | tail -1
    ok "Dependencies installed (python-pptx, pyyaml, Pillow, lxml)"
else
    ok "Dependencies already installed"
fi

# ── Step 3: Skill symlink ──────────────────────────────────────────

header "Claude Code Skill"

if [ -L "$SKILL_DST" ]; then
    # Existing symlink — check if it points to us
    target=$(readlink "$SKILL_DST" 2>/dev/null || true)
    if [ "$target" = "$SKILL_SRC" ]; then
        ok "Skill symlink up to date"
    else
        rm "$SKILL_DST"
        ln -s "$SKILL_SRC" "$SKILL_DST"
        ok "Skill symlink updated (was pointing elsewhere)"
    fi
elif [ -d "$SKILL_DST" ]; then
    warn "Skill directory exists at $SKILL_DST (not a symlink)"
    echo "    Remove it manually if you want the symlink: rm -rf $SKILL_DST"
else
    mkdir -p "$(dirname "$SKILL_DST")"
    # Try symlink first (works on macOS/Linux, needs dev mode on Windows)
    if ln -s "$SKILL_SRC" "$SKILL_DST" 2>/dev/null; then
        ok "Skill symlink created"
    else
        # Windows fallback: copy instead
        cp -r "$SKILL_SRC" "$SKILL_DST"
        ok "Skill copied (symlink not available on this platform)"
        warn "Run setup.sh again after git pull to update the skill"
    fi
fi

# ── Step 4: Optional tools ─────────────────────────────────────────

header "Optional Tools"

LO_PATH=$(find_libreoffice) || true
if [ -n "$LO_PATH" ]; then
    ok "LibreOffice found ($LO_PATH)"
    echo "    Proof images will use LibreOffice for pixel-perfect rendering"
else
    warn "LibreOffice not found"
    echo "    Proof images will use PIL fallback (lower fidelity)"
    echo "    Install from https://www.libreoffice.org/download/"
fi

if command -v gog &>/dev/null; then
    ok "gog CLI found (Google Drive upload available)"
    if [ -n "${GOG_ACCOUNT:-}" ]; then
        ok "GOG_ACCOUNT set ($GOG_ACCOUNT)"
    else
        warn "GOG_ACCOUNT not set — upload will prompt for account"
        echo "    Set it: export GOG_ACCOUNT=you@company.com"
    fi
else
    warn "gog CLI not found (Google Drive upload disabled)"
fi

if command -v claude &>/dev/null; then
    ok "Claude Code found"
    echo "    Use /create-presentation to build research-backed decks"
else
    warn "Claude Code not found"
    echo "    Install from https://claude.ai/claude-code"
    echo "    The builder works standalone, but Claude Code enables AI-driven workflows"
fi

# ── Step 5: Brand onboarding ───────────────────────────────────────

header "Brand Setup"

echo ""
echo "  The builder ships with 6 built-in brands (generic, startup,"
echo "  tech-gradient, academic, government, earth)."
echo ""
echo "  Want to create your company's brand from existing slides?"
echo ""
echo "    1) I have a PPTX template from my company"
echo "    2) I have a folder of company slide decks"
echo "    3) I have both a template and example decks"
echo "    4) Skip — I'll use the built-in brands for now"
echo ""
read -rp "  Choice [4]: " BRAND_CHOICE
BRAND_CHOICE="${BRAND_CHOICE:-4}"

if [ "$BRAND_CHOICE" != "4" ]; then
    echo ""
    read -rp "  Brand name (lowercase, no spaces): " BRAND_NAME

    if [ -z "$BRAND_NAME" ]; then
        warn "No brand name given, skipping"
    else
        ONBOARD_ARGS="--name $BRAND_NAME"

        case "$BRAND_CHOICE" in
            1)
                read -rp "  Path to PPTX template: " TEMPLATE_PATH
                ONBOARD_ARGS="$ONBOARD_ARGS --template $TEMPLATE_PATH"
                ;;
            2)
                read -rp "  Path to folder of PPTX decks: " CORPUS_PATH
                ONBOARD_ARGS="$ONBOARD_ARGS --corpus $CORPUS_PATH"
                ;;
            3)
                read -rp "  Path to PPTX template: " TEMPLATE_PATH
                read -rp "  Path to folder of PPTX decks: " CORPUS_PATH
                ONBOARD_ARGS="$ONBOARD_ARGS --template $TEMPLATE_PATH --corpus $CORPUS_PATH"
                ;;
        esac

        echo ""
        echo "  Launching brand onboarding wizard..."
        echo "  A browser window will open for you to review and customize."
        echo ""
        "$PYTHON_CMD" "$SCRIPT_DIR/onboard_cli.py" $ONBOARD_ARGS || true
    fi
fi

# ── Done ────────────────────────────────────────────────────────────

header "Setup Complete"
echo ""
echo "  Build your first deck:"
echo "    $VENV_DIR/bin/python3 build_deck.py examples/showcase-generic.yaml"
echo ""
echo "  Build with proof images:"
echo "    $VENV_DIR/bin/python3 test_deck.py examples/showcase-generic.yaml --proof-images"
echo ""
if command -v claude &>/dev/null; then
    echo "  Or use Claude Code:"
    echo "    /create-presentation \"Your Topic\" \"Your Audience\""
    echo ""
fi
