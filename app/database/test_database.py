from database import Database


database = Database()

database.add_clipboard_item("Docker")
database.add_clipboard_item("BoardFlow")
database.add_clipboard_item("Python")

items = database.get_clipboard_items()

for item in items:
    print(item)

database.close()