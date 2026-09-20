import sys

from PySide6.QtCore import Qt, QLockFile
from PySide6.QtGui import QAction, QIcon
from PySide6.QtNetwork import QLocalServer
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from app.clipboard.manager import ClipboardManager
from app.clipboard.monitor import ClipboardMonitor
from app.database.database import Database
from app.ipc import request_show
from app.paths import LOCK_FILE, SHOW_SOCKET, ensure_runtime_dirs
from app.ui.styles import DARK_THEME

PREVIEW_LIMIT = 400


def _preview(content, created_at=None):
    text = content.replace("\r\n", "\n")
    if len(text) > PREVIEW_LIMIT:
        text = text[:PREVIEW_LIMIT] + "…"
    if created_at:
        return f"{text}\n{created_at}"
    return text


class MainWindow(QMainWindow):
    def __init__(self, database, tray_available=False):
        super().__init__()

        self.database = database
        self.tray_available = tray_available
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
        self._populate_list(self.database.get_clipboard_items())

    def _populate_list(self, items):
        self.history_list.clear()
        for item in items:
            _, content, created_at = item
            list_item = QListWidgetItem(_preview(content, created_at))
            list_item.setData(Qt.UserRole, content)
            self.history_list.addItem(list_item)

    def handle_search(self, query):
        query = query.strip()
        if not query:
            items = self.database.get_clipboard_items()
        else:
            items = self.database.search_clipboard_items(query)
        self._populate_list(items)

    def handle_new_clipboard(self, text):
        row = self.database.add_clipboard_item(text)
        if row is None:
            return

        query = self.search_field.text().strip()
        if query:
            self._populate_list(self.database.search_clipboard_items(query))
            return

        _, content, created_at = row
        list_item = QListWidgetItem(_preview(content, created_at))
        list_item.setData(Qt.UserRole, content)
        self.history_list.insertItem(0, list_item)

    def handle_item_clicked(self, item):
        text = item.data(Qt.UserRole)
        if not text:
            return
        self.monitor.ignore_next(text)
        self.manager.copy_text(text)

    def clear_history(self):
        self.database.clear_history()
        self.history_list.clear()
        self.search_field.clear()

    def show_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        if self.tray_available:
            event.ignore()
            self.hide()
            return
        event.accept()


def _start_show_server(window):
    QLocalServer.removeServer(str(SHOW_SOCKET))
    SHOW_SOCKET.unlink(missing_ok=True)

    server = QLocalServer(window)
    if not server.listen(str(SHOW_SOCKET)):
        return None

    def accept():
        connection = server.nextPendingConnection()
        if connection is not None:
            connection.close()
        window.show_from_tray()

    server.newConnection.connect(accept)
    return server


def main():
    ensure_runtime_dirs()

    autostart = "--autostart" in sys.argv
    qt_args = [arg for arg in sys.argv if arg != "--autostart"]

    app = QApplication(qt_args)
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(DARK_THEME)

    lock = QLockFile(str(LOCK_FILE))
    lock.setStaleLockTime(5000)
    if not lock.tryLock(100):
        if not autostart:
            try:
                request_show()
            except OSError:
                pass
        return 0

    database = Database()
    tray_available = QSystemTrayIcon.isSystemTrayAvailable()
    window = MainWindow(database, tray_available=tray_available)
    show_server = _start_show_server(window)

    if tray_available:
        tray_icon = QSystemTrayIcon(QIcon.fromTheme("edit-paste"), app)
        tray_menu = QMenu()

        show_action = QAction("Show BoardFlow", tray_icon)
        show_action.triggered.connect(window.show_from_tray)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()

        quit_action = QAction("Quit", tray_icon)
        quit_action.triggered.connect(app.quit)
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.activated.connect(
            lambda reason: window.show_from_tray()
            if reason == QSystemTrayIcon.ActivationReason.DoubleClick
            else None
        )
        tray_icon.show()
        if not autostart:
            tray_icon.showMessage(
                "BoardFlow",
                "Running in the background",
                QSystemTrayIcon.MessageIcon.Information,
                2000,
            )

    def cleanup():
        window.monitor.stop()
        if show_server is not None:
            show_server.close()
        QLocalServer.removeServer(str(SHOW_SOCKET))
        SHOW_SOCKET.unlink(missing_ok=True)
        database.close()
        lock.unlock()

    app.aboutToQuit.connect(cleanup)
    if not autostart:
        window.show()
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, "BoardFlow", f"BoardFlow failed to start:\n{exc}")
        sys.exit(1)
