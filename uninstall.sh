#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -x "$SCRIPT_DIR/venv/bin/python" ]]; then
  PYTHON="$SCRIPT_DIR/venv/bin/python"
else
  PYTHON="$(command -v python3)"
fi

echo "Uninstalling BoardFlow..."

echo "Removing autostart..."
"$PYTHON" -c "from app.autostart import uninstall_autostart; uninstall_autostart()"
echo "Autostart removed."

echo "Unregistering global shortcut..."
"$PYTHON" -c "from app.shortcut import unregister_shortcut; unregister_shortcut()"
echo "Global shortcut unregistered."

rm -rf ~/.cache/boardflow
rm -f "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/boardflow.show.sock"

echo ""
echo "Uninstall complete."
echo "Clipboard history in ~/.local/share/boardflow was left in place."
