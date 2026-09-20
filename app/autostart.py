import subprocess
from pathlib import Path

from app.paths import LAUNCHER_SCRIPT, PROJECT_ROOT

AUTOSTART_DIR = Path.home() / ".config" / "autostart"
AUTOSTART_FILE = AUTOSTART_DIR / "boardflow.desktop"
SYSTEMD_DIR = Path.home() / ".config" / "systemd" / "user"
SYSTEMD_UNIT = SYSTEMD_DIR / "boardflow.service"


def _desktop_entry():
    return f"""[Desktop Entry]
Type=Application
Name=BoardFlow
Comment=BoardFlow Clipboard Manager
Exec={LAUNCHER_SCRIPT} --autostart
Path={PROJECT_ROOT}
Hidden=false
NoDisplay=false
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=5
X-GNOME-UsesNotifications=true
"""


def _systemd_unit():
    return f"""[Unit]
Description=BoardFlow clipboard manager
After=graphical-session.target

[Service]
Type=simple
WorkingDirectory={PROJECT_ROOT}
ExecStart={LAUNCHER_SCRIPT} --autostart
Restart=on-failure
RestartSec=4
KillMode=process

[Install]
WantedBy=default.target
WantedBy=graphical-session.target
"""


def _systemctl(*args):
    subprocess.run(
        ["systemctl", "--user", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def install_autostart():
    AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
    SYSTEMD_DIR.mkdir(parents=True, exist_ok=True)
    LAUNCHER_SCRIPT.chmod(LAUNCHER_SCRIPT.stat().st_mode | 0o111)

    AUTOSTART_FILE.write_text(_desktop_entry())
    AUTOSTART_FILE.chmod(AUTOSTART_FILE.stat().st_mode | 0o111)

    SYSTEMD_UNIT.write_text(_systemd_unit())
    _systemctl("daemon-reload")
    _systemctl("enable", "boardflow.service")
    return True


def uninstall_autostart():
    _systemctl("disable", "--now", "boardflow.service")
    if SYSTEMD_UNIT.exists():
        SYSTEMD_UNIT.unlink()
    _systemctl("daemon-reload")
    if AUTOSTART_FILE.exists():
        AUTOSTART_FILE.unlink()
    return True
