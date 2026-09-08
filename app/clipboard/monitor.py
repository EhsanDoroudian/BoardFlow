import subprocess

from PySide6.QtCore import QObject, QTimer, Signal


class ClipboardMonitor(QObject):
    text_copied = Signal(str)

    def __init__(self):
        super().__init__()

        self.last_text = ""

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)

    def start(self):
        self.timer.start(300)

    def stop(self):
        self.timer.stop()

    def check_clipboard(self):
        result = subprocess.run(
            ["wl-paste", "--no-newline"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return

        text = result.stdout

        if not text:
            return

        if text == self.last_text:
            return

        self.last_text = text
        self.text_copied.emit(text)