import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from app.ui.styles import DARK_THEME, LIGHT_THEME


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BoardFlow")
        self.resize(800, 500)

        self.dark_mode = True

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        title = QLabel("BoardFlow")
        title.setObjectName("title")

        search = QLineEdit()
        search.setPlaceholderText("Search clipboard history...")

        history_title = QLabel("Clipboard History")
        history_title.setObjectName("history_title")

        theme_button = QPushButton("☀")
        theme_button.setFixedSize(40, 40)
        theme_button.clicked.connect(self.toggle_theme)

        layout.addWidget(theme_button)
        layout.addWidget(title)
        layout.addWidget(search)
        layout.addWidget(history_title)
        layout.addStretch()

        self.setCentralWidget(central_widget)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(DARK_THEME)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()