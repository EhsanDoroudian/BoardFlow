from .database import Database


database = Database()

database.add_clipboard_item("Docker")
database.add_clipboard_item("BoardFlow")
database.add_clipboard_item("Python")

print("Before clearing:")
print(database.get_clipboard_items())

database.clear_history()

print("After clearing:")
print(database.get_clipboard_items())

database.close()