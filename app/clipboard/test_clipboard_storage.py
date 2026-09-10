import sys

from PySide6.QtWidgets import QApplication

from app.clipboard.monitor import ClipboardMonitor
from app.database.database import Database


def on_text_copied(text):
    database.add_clipboard_item(text)
    print(f"Saved: {text}", flush=True)


app = QApplication(sys.argv)

database = Database()

monitor = ClipboardMonitor()
monitor.text_copied.connect(on_text_copied)

monitor.start()

print("BoardFlow clipboard storage is running...", flush=True)

sys.exit(app.exec())