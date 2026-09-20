import shutil
import subprocess
import threading

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtDBus import QDBusConnection, QDBusInterface
from PySide6.QtGui import QClipboard, QGuiApplication

IDLE_MS = 1200
IDLE_POLL_MS = 400


def read_clipboard_text():
    wl_paste = shutil.which("wl-paste")
    if not wl_paste:
        return None

    try:
        result = subprocess.run(
            [wl_paste, "--type", "text/plain", "--no-newline"],
            capture_output=True,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None

    try:
        text = result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None

    return text or None


class ClipboardMonitor(QObject):
    text_copied = Signal(str)

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._last_text = ""
        self._ignored_text = None
        self._was_idle = False
        self._idle_iface = None
        self._timer = QTimer(self)
        self._timer.setInterval(IDLE_POLL_MS)
        self._timer.timeout.connect(self._on_idle_tick)

    def start(self):
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None:
            clipboard.dataChanged.connect(self._on_qt_clipboard)

        bus = QDBusConnection.sessionBus()
        if bus.isConnected():
            iface = QDBusInterface(
                "org.gnome.Mutter.IdleMonitor",
                "/org/gnome/Mutter/IdleMonitor/Core",
                "org.gnome.Mutter.IdleMonitor",
                bus,
            )
            if iface.isValid():
                self._idle_iface = iface

        self._timer.start()

    def stop(self):
        self._timer.stop()

    def ignore_next(self, text):
        with self._lock:
            self._ignored_text = text

    def _idle_time_ms(self):
        if self._idle_iface is None:
            return 0
        reply = self._idle_iface.call("GetIdletime")
        args = reply.arguments()
        if not args:
            return 0
        try:
            return int(args[0])
        except (TypeError, ValueError):
            return 0

    def _on_idle_tick(self):
        is_idle = self._idle_time_ms() >= IDLE_MS
        if is_idle and not self._was_idle:
            self._capture()
        self._was_idle = is_idle

    def _on_qt_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        if clipboard is None:
            return
        text = clipboard.text(QClipboard.Mode.Clipboard)
        if text:
            self._maybe_emit(text)

    def _capture(self):
        text = read_clipboard_text()
        if text:
            self._maybe_emit(text)

    def _maybe_emit(self, text):
        with self._lock:
            if text == self._last_text:
                return
            self._last_text = text
            if text == self._ignored_text:
                self._ignored_text = None
                return
        self.text_copied.emit(text)
