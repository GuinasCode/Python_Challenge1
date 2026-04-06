import sqlite3
from pathlib import Path

from app.utils import build_placeholder_image, category_order, guess_category_name

DB_PATH = Path(__file__).resolve().parent / "restaurante.db"


def table_columns(cursor: sqlite3.Cursor, table_name: str) -> set[str]:
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def ensure_base_tables(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            ordem INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            nome_cliente TEXT NOT NULL,
            itens TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            valor_total REAL NOT NULL,
            order_items TEXT
        );

        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria_id INTEGER REFERENCES categories(id),
            imagem_base64 TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            perfil TEXT NOT NULL DEFAULT 'garcom' CHECK (perfil IN ('admin', 'gerente', 'garcom', 'cozinha')),
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )


def migrate_legacy_schema(cursor: sqlite3.Cursor):
    menu_columns = table_columns(cursor, "menu")
    if "categoria_id" not in menu_columns:
        cursor.execute("ALTER TABLE menu ADD COLUMN categoria_id INTEGER")
    if "imagem_base64" not in menu_columns:
        cursor.execute("ALTER TABLE menu ADD COLUMN imagem_base64 TEXT")

    order_columns = table_columns(cursor, "orders")
    if "order_items" not in order_columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN order_items TEXT")

    category_defaults = [
        ("Pratos executivos", category_order("Pratos executivos")),
        ("Bebidas", category_order("Bebidas")),
        ("Sobremesas", category_order("Sobremesas")),
        ("Sem categoria", category_order("Sem categoria")),
    ]
    for nome, ordem in category_defaults:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (nome, ordem) VALUES (?, ?)",
            (nome, ordem),
        )
        cursor.execute(
            "UPDATE categories SET ordem = ? WHERE nome = ? AND (ordem IS NULL OR ordem = 0)",
            (ordem, nome),
        )

    cursor.execute("SELECT id, nome FROM categories")
    categories_by_name = {row[1]: row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT id, item, categoria_id, imagem_base64 FROM menu")
    for item_id, item_name, categoria_id, imagem_base64 in cursor.fetchall():
        if categoria_id is None:
            guessed_category = guess_category_name(item_name)
            cursor.execute(
                "UPDATE menu SET categoria_id = ? WHERE id = ?",
                (categories_by_name.get(guessed_category, categories_by_name["Sem categoria"]), item_id),
            )
        if not imagem_base64:
            effective_category = guess_category_name(item_name)
            cursor.execute(
                "UPDATE menu SET imagem_base64 = ? WHERE id = ?",
                (build_placeholder_image(item_name, effective_category), item_id),
            )


def create_tables():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    ensure_base_tables(cursor)
    migrate_legacy_schema(cursor)

    connection.commit()
    connection.close()


if __name__ == '__main__':
    create_tables()
    print(f'Banco de dados e tabelas inicializados com sucesso em: {DB_PATH}')
