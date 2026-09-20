import shutil
import sqlite3

from app.paths import DATABASE_PATH, LEGACY_DATABASE_PATH, ensure_runtime_dirs

HISTORY_LIMIT = 500


class Database:
    def __init__(self, path=None):
        ensure_runtime_dirs()
        self.path = path or DATABASE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._migrate_legacy_db()

        self.connection = sqlite3.connect(self.path, check_same_thread=True)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.create_tables()

    def _migrate_legacy_db(self):
        if self.path.exists() or not LEGACY_DATABASE_PATH.exists():
            return
        shutil.copy2(LEGACY_DATABASE_PATH, self.path)

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
        last = self.connection.execute(
            """
            SELECT content FROM clipboard_items
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
        if last and last[0] == content:
            return None

        cursor = self.connection.execute(
            """
            INSERT INTO clipboard_items (content)
            VALUES (?)
            """,
            (content,),
        )
        self.connection.execute(
            """
            DELETE FROM clipboard_items
            WHERE id NOT IN (
                SELECT id FROM clipboard_items
                ORDER BY id DESC
                LIMIT ?
            )
            """,
            (HISTORY_LIMIT,),
        )
        self.connection.commit()

        return self.connection.execute(
            """
            SELECT id, content, created_at
            FROM clipboard_items
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    def get_clipboard_items(self):
        cursor = self.connection.execute(
            """
            SELECT id, content, created_at
            FROM clipboard_items
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()

    def search_clipboard_items(self, query):
        escaped = query.replace("%", "#%").replace("_", "#_")
        cursor = self.connection.execute(
            """
            SELECT id, content, created_at
            FROM clipboard_items
            WHERE content LIKE ? ESCAPE '#'
            ORDER BY id DESC
            """,
            (f"%{escaped}%",),
        )
        return cursor.fetchall()

    def clear_history(self):
        self.connection.execute("DELETE FROM clipboard_items")
        self.connection.commit()

    def close(self):
        self.connection.close()
