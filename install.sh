#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -x "$SCRIPT_DIR/venv/bin/python" ]]; then
  PYTHON="$SCRIPT_DIR/venv/bin/python"
else
  PYTHON="$(command -v python3)"
fi

chmod +x "$SCRIPT_DIR/scripts/boardflow-run.sh" "$SCRIPT_DIR/scripts/boardflow-shortcut.py"

echo "Installing BoardFlow..."

echo "Setting up autostart..."
"$PYTHON" -c "from app.autostart import install_autostart; install_autostart()"
echo "Autostart installed:"
echo "  ~/.config/autostart/boardflow.desktop"
echo "  ~/.config/systemd/user/boardflow.service"

echo "Registering global shortcut (Ctrl+Shift+V)..."
"$PYTHON" -c "from app.shortcut import register_shortcut; register_shortcut()"
echo "Global shortcut registered."

echo ""
echo "Installation complete."
echo "BoardFlow will:"
echo "  - Start automatically on login (using the project venv)"
echo "  - Run in the system tray when available"
echo "  - Show the window with Ctrl+Shift+V"
echo ""
echo "To start BoardFlow now:"
echo "  ./scripts/boardflow-run.sh"
