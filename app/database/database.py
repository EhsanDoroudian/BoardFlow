import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "boardflow.db"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)

        self.create_tables()

    def create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS clipboard_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def add_clipboard_item(self, content):
        self.connection.execute(
            """
            INSERT INTO clipboard_items (content)
            VALUES (?)
            """,
            (content,),
        )

        self.connection.commit()

    def get_clipboard_items(self):
        cursor = self.connection.execute(
            """
            SELECT id, content, created_at
            FROM clipboard_items
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()
    
    def clear_history(self):
        self.connection.execute(
            """
            DELETE FROM clipboard_items
            """
        )

        self.connection.commit()
        
    def close(self):
        self.connection.close()