import sys

from PySide6.QtWidgets import QApplication

from monitor import ClipboardMonitor


def on_text_copied(text):
    print(f"Copied: {text}", flush=True)


app = QApplication(sys.argv)

monitor = ClipboardMonitor()
monitor.text_copied.connect(on_text_copied)

monitor.start()

print("Clipboard monitor is running...", flush=True)

sys.exit(app.exec())