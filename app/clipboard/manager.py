from PySide6.QtGui import QClipboard, QGuiApplication


class ClipboardManager:
    def copy_text(self, text):
        app = QGuiApplication.instance()
        if app is None:
            return False
        clipboard = app.clipboard()
        if clipboard is None:
            return False
        clipboard.setText(text, QClipboard.Mode.Clipboard)
        return True
