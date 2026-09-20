# BoardFlow

A small clipboard history manager for Linux Wayland desktops.

## Features

- Monitor clipboard changes automatically
- Store clipboard history in a local SQLite database
- Search through clipboard history
- Restore any previous clipboard item with one click
- Support for multiline and Unicode text
- System tray integration (runs in background)
- Global shortcut: `Ctrl+Shift+V` to show the window
- Autostart on login

## Requirements

- Python 3.12+
- Wayland desktop environment (Ubuntu 24)
- `wl-clipboard` system package (provides `wl-copy` and `wl-paste`)

### Installing system dependencies

```bash
sudo apt install wl-clipboard
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd BoardFlow

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

```bash
./scripts/boardflow-run.sh
```

Or with the venv active:

```bash
python -m app.main
```

BoardFlow will start monitoring your clipboard. Copy any text and it will appear in the history list. Click any item to restore it to your clipboard.

Start it with `venv/bin/python` (or the launcher script). System `python3` does not have PySide6, so login autostart used to fail immediately.

### System Tray

BoardFlow runs in the system tray. Closing the window hides it to the tray instead of quitting. Double-click the tray icon or use the tray menu to show the window.

### Global Shortcut

Press `Ctrl+Shift+V` anywhere on the desktop to show BoardFlow.

### Autostart

`./install.sh` enables login autostart (GNOME Startup Applications plus a user systemd service). After a reboot BoardFlow starts in the background; press `Ctrl+Shift+V` to show it.

To disable autostart:

```bash
./uninstall.sh
```

This creates/removes `~/.config/autostart/boardflow.desktop` and registers/unregisters the global shortcut.
