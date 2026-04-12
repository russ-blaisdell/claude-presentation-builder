#!/usr/bin/env bash
#
# Claude Pres Builder — Uninstall
#
# Removes everything created by setup.sh so you can test a fresh setup.
# Does NOT delete repo files, built-in brands, or your source code.
#
# Usage:  ./uninstall.sh           # interactive — confirms before each step
#         ./uninstall.sh --force   # non-interactive — removes everything silently
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
SKILL_DST="$HOME/.claude/skills/create-presentation"
FORCE=false

if [ "${1:-}" = "--force" ]; then
    FORCE=true
fi

# Colors
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    RED='\033[0;31m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    GREEN='' YELLOW='' RED='' BOLD='' NC=''
fi

removed() { echo -e "${GREEN}[REMOVED]${NC}  $1"; }
skipped() { echo -e "${YELLOW}[SKIPPED]${NC}  $1"; }

confirm() {
    if [ "$FORCE" = true ]; then
        return 0
    fi
    read -rp "  $1 (y/N): " answer
    [[ "$answer" =~ ^[Yy] ]]
}

echo ""
echo "======================================"
echo "  Claude Pres Builder — Uninstall"
echo "======================================"
echo ""

# ── 1. Virtual environment ──────────────────────────────────────────

if [ -d "$VENV_DIR" ]; then
    if confirm "Remove Python virtual environment (.venv/)?"; then
        rm -rf "$VENV_DIR"
        removed "Virtual environment (.venv/)"
    else
        skipped "Virtual environment"
    fi
else
    skipped "Virtual environment (not found)"
fi

# ── 2. Skill symlink ───────────────────────────────────────────────

if [ -L "$SKILL_DST" ]; then
    if confirm "Remove skill symlink ($SKILL_DST)?"; then
        rm "$SKILL_DST"
        removed "Skill symlink"
    else
        skipped "Skill symlink"
    fi
elif [ -d "$SKILL_DST" ]; then
    if confirm "Remove skill directory ($SKILL_DST)?"; then
        rm -rf "$SKILL_DST"
        removed "Skill directory (was a copy, not symlink)"
    else
        skipped "Skill directory"
    fi
else
    skipped "Skill symlink (not found)"
fi

# ── 3. User-created brands ─────────────────────────────────────────

BUILTIN_BRANDS="generic startup academic government tech-gradient earth"
USER_BRANDS=()

if [ -d "$SCRIPT_DIR/brands" ]; then
    for brand_dir in "$SCRIPT_DIR/brands"/*/; do
        brand_name=$(basename "$brand_dir")
        is_builtin=false
        for b in $BUILTIN_BRANDS; do
            if [ "$brand_name" = "$b" ]; then
                is_builtin=true
                break
            fi
        done
        if [ "$is_builtin" = false ]; then
            USER_BRANDS+=("$brand_name")
        fi
    done
fi

if [ ${#USER_BRANDS[@]} -gt 0 ]; then
    echo ""
    echo "  Found user-created brands: ${USER_BRANDS[*]}"
    if confirm "Remove user-created brands?"; then
        for brand_name in "${USER_BRANDS[@]}"; do
            rm -rf "$SCRIPT_DIR/brands/$brand_name"
            removed "Brand: $brand_name"
        done
    else
        skipped "User-created brands"
    fi
else
    skipped "User-created brands (none found)"
fi

# ── 4. Build artifacts ──────────────────────────────────────────────

# Proof directories and QA reports in the repo root
ARTIFACTS=0
for pattern in "$SCRIPT_DIR"/*-proof/ "$SCRIPT_DIR"/*-qa-report.json "$SCRIPT_DIR"/*-qa-report.md "$SCRIPT_DIR"/*-proof.md; do
    for f in $pattern; do
        [ -e "$f" ] && ARTIFACTS=$((ARTIFACTS + 1))
    done
done

if [ "$ARTIFACTS" -gt 0 ]; then
    if confirm "Remove build artifacts (proof dirs, QA reports)?"; then
        rm -rf "$SCRIPT_DIR"/*-proof/ 2>/dev/null || true
        rm -f "$SCRIPT_DIR"/*-qa-report.json 2>/dev/null || true
        rm -f "$SCRIPT_DIR"/*-qa-report.md 2>/dev/null || true
        rm -f "$SCRIPT_DIR"/*-proof.md 2>/dev/null || true
        removed "Build artifacts"
    else
        skipped "Build artifacts"
    fi
else
    skipped "Build artifacts (none found)"
fi

# ── 5. Python cache ─────────────────────────────────────────────────

if [ -d "$SCRIPT_DIR/__pycache__" ] || [ -d "$SCRIPT_DIR/diagrams/__pycache__" ]; then
    if confirm "Remove Python cache (__pycache__)?"; then
        find "$SCRIPT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find "$SCRIPT_DIR" -name "*.pyc" -delete 2>/dev/null || true
        removed "Python cache"
    else
        skipped "Python cache"
    fi
else
    skipped "Python cache (not found)"
fi

# ── Done ────────────────────────────────────────────────────────────

echo ""
echo -e "${BOLD}Uninstall complete.${NC}"
echo ""
echo "  To set up again:  ./setup.sh"
echo ""
echo "  Not removed (repo files):"
echo "    - Source code (*.py, *.md, *.json, *.yaml)"
echo "    - Built-in brands (brands/generic, brands/startup, ...)"
echo "    - Example decks (examples/)"
echo "    - Screenshots (docs/screenshots/)"
echo ""
