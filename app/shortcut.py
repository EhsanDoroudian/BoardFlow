import ast
import shutil
import subprocess
import sys

from app.paths import SHORTCUT_SCRIPT

SHORTCUT_PATH = "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/boardflow/"
SCHEMA_LIST = "org.gnome.settings-daemon.plugins.media-keys"
KEY_LIST = "custom-keybindings"
SCHEMA_ITEM = "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"
SHORTCUT_NAME = "BoardFlow"
SHORTCUT_BINDING = "<Control><Shift>v"


def _gsettings(*args):
    result = subprocess.run(
        ["gsettings", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "gsettings failed").strip()
        raise RuntimeError(message)
    return result.stdout.strip()


def _current_bindings():
    raw = _gsettings("get", SCHEMA_LIST, KEY_LIST)
    try:
        value = ast.literal_eval(raw)
    except (SyntaxError, ValueError):
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def _format_bindings(paths):
    inner = ", ".join(f"'{path}'" for path in paths)
    return f"[{inner}]"


def _shortcut_command():
    python = shutil.which("python3") or sys.executable
    return f"{python} {SHORTCUT_SCRIPT}"


def register_shortcut(script_path=None):
    del script_path
    paths = _current_bindings()
    if SHORTCUT_PATH not in paths:
        paths.append(SHORTCUT_PATH)
        _gsettings("set", SCHEMA_LIST, KEY_LIST, _format_bindings(paths))

    prefix = f"{SCHEMA_ITEM}:{SHORTCUT_PATH}"
    _gsettings("set", prefix, "name", SHORTCUT_NAME)
    _gsettings("set", prefix, "command", _shortcut_command())
    _gsettings("set", prefix, "binding", SHORTCUT_BINDING)
    return True


def unregister_shortcut():
    paths = [path for path in _current_bindings() if path != SHORTCUT_PATH]
    _gsettings("set", SCHEMA_LIST, KEY_LIST, _format_bindings(paths))

    prefix = f"{SCHEMA_ITEM}:{SHORTCUT_PATH}"
    for key, value in (("name", ""), ("command", ""), ("binding", "")):
        try:
            _gsettings("set", prefix, key, value)
        except RuntimeError:
            pass
    return True
