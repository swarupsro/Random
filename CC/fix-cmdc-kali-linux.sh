#!/usr/bin/env bash
set -Eeuo pipefail

# Command Code installer/updater for native Kali Linux (also works in VMs).
# Run as your normal user, not with sudo.

trap 'printf "[ERROR] Failed at line %s.\n" "$LINENO" >&2' ERR

if [[ $EUID -eq 0 ]]; then
  echo '[ERROR] Run as your normal user, not root or sudo.' >&2
  exit 1
fi

if [[ ! -r /etc/os-release ]]; then
  echo '[ERROR] Cannot identify this Linux distribution.' >&2
  exit 1
fi
. /etc/os-release
if [[ "${ID:-}" != kali ]]; then
  printf '[WARNING] Detected %s, not Kali Linux. Continue? [y/N] ' "${PRETTY_NAME:-unknown}"
  read -r answer
  [[ $answer =~ ^[Yy]$ ]] || exit 1
fi

echo '=== Command Code: native Kali Linux setup ==='
if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  echo '[+] Installing missing Node.js/npm from Kali repositories...'
  sudo apt-get update
  sudo apt-get install -y nodejs npm
fi

printf '[+] Node: %s | npm: %s\n' "$(node --version)" "$(npm --version)"

# Keep global npm installs in the user's home directory.
NPM_GLOBAL="$HOME/.npm-global"
mkdir -p "$NPM_GLOBAL/bin"
npm config set prefix "$NPM_GLOBAL" --location=user
export PATH="$NPM_GLOBAL/bin:$PATH"

# Configure both supported interactive shells; avoid duplicate entries.
PATH_LINE='export PATH="$HOME/.npm-global/bin:$PATH"'
for rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
  touch "$rc"
  if ! grep -Fxq "$PATH_LINE" "$rc"; then
    printf '\n# User-owned global npm executables\n%s\n' "$PATH_LINE" >> "$rc"
    printf '[+] Configured %s\n' "$rc"
  fi
done

# A system-wide installation is deliberately left untouched. User PATH
# takes precedence, so no unrelated or system-managed files are deleted.
if [[ -e /usr/local/bin/cmd || -L /usr/local/bin/cmd ]]; then
  echo '[INFO] Existing /usr/local/bin/cmd left unchanged.'
fi

printf '[+] Installing/updating command-code in %s ...\n' "$NPM_GLOBAL"
npm install --global command-code@latest

# Check the actual executable in the configured npm prefix.
CMD_BIN="$NPM_GLOBAL/bin/cmd"
if [[ ! -x "$CMD_BIN" ]]; then
  echo '[ERROR] npm completed, but the expected cmd executable was not found.' >&2
  echo '[INFO] Inspect npm package metadata: npm view command-code bin' >&2
  exit 1
fi

hash -r 2>/dev/null || true
printf '\n[+] Executable: %s\n' "$CMD_BIN"
printf '[+] Version: '
"$CMD_BIN" --version
printf '[+] Resolved command: %s\n' "$(command -v cmd)"
printf '\n[OK] Finished. Open a new terminal or run: source ~/.zshrc\n'
printf '[INFO] Future update: npm install -g command-code@latest\n'
