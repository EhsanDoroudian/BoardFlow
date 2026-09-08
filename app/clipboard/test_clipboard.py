import sys

from PySide6.QtWidgets import QApplication


app = QApplication(sys.argv)

clipboard = app.clipboard()

print("Clipboard content:")
print(clipboard.text())

sys.exit()