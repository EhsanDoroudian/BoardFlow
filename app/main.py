import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.database.database import Database
from app.ui.styles import DARK_THEME
from app.clipboard.monitor import ClipboardMonitor
from app.clipboard.manager import ClipboardManager

class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.database = database
        self.monitor = ClipboardMonitor()
        self.manager = ClipboardManager()

        self.setWindowTitle("BoardFlow")
        self.resize(800, 500)

        self.setup_ui()
        self.load_history()

        self.monitor.text_copied.connect(self.handle_new_clipboard)
        self.history_list.itemClicked.connect(self.handle_item_clicked)
        self.monitor.start()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        title = QLabel("BoardFlow")
        title.setObjectName("title")

        search = QLineEdit()
        search.setPlaceholderText("Search clipboard history...")

        history_title = QLabel("Clipboard History")
        history_title.setObjectName("history_title")

        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(self.clear_history)

        history_list = QListWidget()
        history_list.setObjectName("history_list")

        layout.addWidget(title)
        layout.addWidget(search)
        layout.addWidget(history_title)
        layout.addWidget(clear_button)
        layout.addWidget(history_list)

        self.history_list = history_list

        self.setCentralWidget(central_widget)

    def load_history(self):
        items = self.database.get_clipboard_items()

        for item in items:
            _, content, created_at = item

            self.history_list.addItem(
                f"{content}\n{created_at}"
            )
            
    def handle_new_clipboard(self, text):
        self.database.add_clipboard_item(text)

        self.history_list.insertItem(0, text)

    def handle_item_clicked(self, item):
        text = item.text().split("\n")[0]

        self.monitor.ignore_next(text)
        self.manager.copy_text(text)

    def clear_history(self):
        self.database.clear_history()
        self.history_list.clear()

def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(DARK_THEME)

    database = Database()

    window = MainWindow(database)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()