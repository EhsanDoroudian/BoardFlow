import sys

from PySide6.QtCore import Qt
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
        search.textChanged.connect(self.handle_search)

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
        self.search_field = search

        self.setCentralWidget(central_widget)

    def load_history(self):
        items = self.database.get_clipboard_items()
        self._populate_list(items)

    def _populate_list(self, items):
        self.history_list.clear()

        for item in items:
            _, content, created_at = item
            list_item = QListWidgetItem(f"{content}\n{created_at}")
            list_item.setData(Qt.UserRole, content)
            self.history_list.addItem(list_item)
            
    def handle_search(self, query):
        if not query.strip():
            items = self.database.get_clipboard_items()
        else:
            items = self.database.search_clipboard_items(query.strip())

        self._populate_list(items)

    def handle_new_clipboard(self, text):
        self.database.add_clipboard_item(text)

        query = self.search_field.text().strip()
        if query:
            items = self.database.search_clipboard_items(query)
            self._populate_list(items)
        else:
            list_item = QListWidgetItem(text)
            list_item.setData(Qt.UserRole, text)
            self.history_list.insertItem(0, list_item)

    def handle_item_clicked(self, item):
        text = item.data(Qt.UserRole)

        self.monitor.ignore_next(text)
        self.manager.copy_text(text)

    def clear_history(self):
        self.database.clear_history()
        self.history_list.clear()
        self.search_field.clear()

def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(DARK_THEME)

    database = Database()

    window = MainWindow(database)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()