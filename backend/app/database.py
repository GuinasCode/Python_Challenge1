import os
import sqlite3
from typing import Any, Iterable

DEFAULT_DB = os.getenv("RESTAURANTE_DB", os.path.join(os.path.dirname(os.path.dirname(__file__)), "restaurante.db"))


class DatabaseManager:
    def __init__(self, db_name: str | None = None):
        self.db_path = db_name or DEFAULT_DB
        self.connection: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self

    def execute_query(self, query: str, params: tuple[Any, ...] | None = None):
        if not self.connection:
            self.connect()
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute_non_query(self, query: str, params: tuple[Any, ...] | None = None):
        if not self.connection:
            self.connect()
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor

    def execute_many(self, query: str, params_list: Iterable[tuple[Any, ...]]):
        if not self.connection:
            self.connect()
        self.cursor.executemany(query, params_list)
        return self.cursor

    def commit(self):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        self.close()
