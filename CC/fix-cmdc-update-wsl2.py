#!/usr/bin/env bash

set -e

echo "=== Command Code WSL2 Kali Setup ==="

# Check required commands
if ! command -v node >/dev/null 2>&1; then
    echo "[!] Node.js not found."
    echo "Install Node.js first, then run this script again."
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "[!] npm not found."
    echo "Install npm first, then run this script again."
    exit 1
fi

echo
echo "[+] Current environment:"
echo "Node : $(node -v)"
echo "npm  : $(npm -v)"
echo "Node path : $(which node)"
echo "npm path  : $(which npm)"
echo "npm prefix: $(npm config get prefix)"

# -------------------------------------------------------
# Configure user-owned npm global directory
# -------------------------------------------------------

NPM_GLOBAL="$HOME/.npm-global"

echo
echo "[+] Creating user-owned npm global directory..."
mkdir -p "$NPM_GLOBAL"

echo "[+] Setting npm global prefix to:"
echo "    $NPM_GLOBAL"

npm config set prefix "$NPM_GLOBAL"

# -------------------------------------------------------
# Detect shell and update PATH permanently
# -------------------------------------------------------

CURRENT_SHELL="$(basename "${SHELL:-/bin/bash}")"

case "$CURRENT_SHELL" in
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    *)
        SHELL_RC="$HOME/.profile"
        ;;
esac

PATH_LINE='export PATH="$HOME/.npm-global/bin:$PATH"'

if ! grep -Fxq "$PATH_LINE" "$SHELL_RC" 2>/dev/null; then
    echo "[+] Adding npm global bin directory to $SHELL_RC"
    echo "" >> "$SHELL_RC"
    echo "# User npm global packages" >> "$SHELL_RC"
    echo "$PATH_LINE" >> "$SHELL_RC"
else
    echo "[+] PATH already configured in $SHELL_RC"
fi

# Apply PATH immediately
export PATH="$HOME/.npm-global/bin:$PATH"

# -------------------------------------------------------
# Remove old system-wide Command Code installation
# -------------------------------------------------------

echo
echo "[+] Checking old system-wide Command Code installation..."

if [ -e "/usr/local/lib/node_modules/command-code" ] || \
   [ -e "/usr/local/bin/cmd" ]; then

    echo "[!] Old Command Code installation found under /usr/local"
    echo "[+] Removing old system-wide installation..."

    sudo npm uninstall -g command-code --prefix /usr/local || true

    # Remove stale symlink if npm left one behind
    if [ -L "/usr/local/bin/cmd" ]; then
        sudo rm -f /usr/local/bin/cmd
    fi

else
    echo "[+] No old /usr/local Command Code installation found."
fi

# -------------------------------------------------------
# Install latest Command Code
# -------------------------------------------------------

echo
echo "[+] Installing latest Command Code..."

npm install -g command-code@latest

# Refresh command cache
hash -r 2>/dev/null || true
rehash 2>/dev/null || true

# -------------------------------------------------------
# Verify
# -------------------------------------------------------

echo
echo "=============================================="
echo " Installation completed"
echo "=============================================="

echo
echo "Node:"
node -v

echo
echo "npm:"
npm -v

echo
echo "npm global prefix:"
npm config get prefix

echo
echo "npm global root:"
npm root -g

echo
echo "Command Code path:"
command -v cmd || true

echo
echo "Command Code version:"
cmd --version || true

echo
echo "Expected Command Code path:"
echo "$HOME/.npm-global/bin/cmd"

echo
echo "Done."
echo
echo "Future updates:"
echo "  npm install -g command-code@latest"
echo
echo "Do NOT use sudo with normal Command Code updates."