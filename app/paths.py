import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = Path.home() / ".cache" / "boardflow"
DATA_DIR = Path.home() / ".local" / "share" / "boardflow"
LOCK_FILE = CACHE_DIR / "boardflow.lock"
DATABASE_PATH = DATA_DIR / "boardflow.db"
LEGACY_DATABASE_PATH = Path(__file__).resolve().parent / "database" / "boardflow.db"
VENV_PYTHON = PROJECT_ROOT / "venv" / "bin" / "python"
LAUNCHER_SCRIPT = PROJECT_ROOT / "scripts" / "boardflow-run.sh"
SHORTCUT_SCRIPT = PROJECT_ROOT / "scripts" / "boardflow-shortcut.py"
RUNTIME_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", str(CACHE_DIR)))
SHOW_SOCKET = RUNTIME_DIR / "boardflow.show.sock"


def ensure_runtime_dirs():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def app_python():
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return shutil.which("python3") or "python3"
