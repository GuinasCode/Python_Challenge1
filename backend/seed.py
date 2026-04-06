from passlib.hash import bcrypt

from app.database import DatabaseManager
from app.utils import build_placeholder_image, category_order

CATEGORIES = [
    ("Pratos executivos", category_order("Pratos executivos")),
    ("Bebidas", category_order("Bebidas")),
    ("Sobremesas", category_order("Sobremesas")),
    ("Sem categoria", category_order("Sem categoria")),
]

MENU_ITEMS = [
    ("Pratos executivos", "Frango Grelhado", 32.90),
    ("Pratos executivos", "Filé ao Molho Madeira", 48.90),
    ("Pratos executivos", "Massa ao Sugo", 28.50),
    ("Pratos executivos", "Salmão ao Limão", 59.90),
    ("Pratos executivos", "Risoto de Cogumelos", 42.00),
    ("Bebidas", "Coca-Cola 350ml", 6.00),
    ("Bebidas", "Suco Natural 500ml", 9.00),
    ("Bebidas", "Água Mineral", 4.00),
    ("Sobremesas", "Petit Gateau", 18.00),
    ("Sobremesas", "Mousse de Maracujá", 14.00),
]

USERS = [
    ("gerente", "Gerente", "gerente@restaurante.com", "gerente123", "gerente"),
    ("garcom", "Garçom", "garcom@restaurante.com", "garcom123", "garcom"),
    ("cozinha", "Cozinha", "cozinha@restaurante.com", "cozinha123", "cozinha"),
]


def seed_categories():
    with DatabaseManager() as db:
        for nome, ordem in CATEGORIES:
            db.execute_non_query(
                "INSERT OR IGNORE INTO categories (nome, ordem) VALUES (?, ?)",
                (nome, ordem),
            )
            db.execute_non_query(
                "UPDATE categories SET ordem = ? WHERE nome = ? AND (ordem IS NULL OR ordem = 0)",
                (ordem, nome),
            )


def seed_menu():
    with DatabaseManager() as db:
        categories = {
            row["nome"]: row["id"]
            for row in db.execute_query("SELECT id, nome FROM categories")
        }

        for category_name, item_name, price in MENU_ITEMS:
            existing = db.execute_query(
                "SELECT id, categoria_id, imagem_base64 FROM menu WHERE item = ?",
                (item_name,),
            )
            image = build_placeholder_image(item_name, category_name)
            if not existing:
                db.execute_non_query(
                    "INSERT INTO menu (item, valor, categoria_id, imagem_base64) VALUES (?, ?, ?, ?)",
                    (item_name, price, categories[category_name], image),
                )
                continue

            row = existing[0]
            db.execute_non_query(
                """
                UPDATE menu
                SET valor = ?,
                    categoria_id = COALESCE(categoria_id, ?),
                    imagem_base64 = CASE
                        WHEN imagem_base64 IS NULL OR TRIM(imagem_base64) = '' THEN ?
                        ELSE imagem_base64
                    END
                WHERE id = ?
                """,
                (price, categories[category_name], image, row["id"]),
            )


def create_admin():
    senha_hash = bcrypt.hash('admin123')
    with DatabaseManager() as db:
        db.execute_non_query(
            '''INSERT OR IGNORE INTO users
            (login, nome, email, senha_hash, perfil)
            VALUES (?, ?, ?, ?, ?)''',
            ('admin', 'Administrador', 'admin@restaurante.com', senha_hash, 'admin')
        )


def seed_users():
    with DatabaseManager() as db:
        for login, nome, email, senha, perfil in USERS:
            db.execute_non_query(
                '''INSERT OR IGNORE INTO users (login, nome, email, senha_hash, perfil)
                VALUES (?, ?, ?, ?, ?)''',
                (login, nome, email, bcrypt.hash(senha), perfil),
            )


def seed():
    seed_categories()
    seed_menu()
    create_admin()
    seed_users()


if __name__ == "__main__":
    seed()
    print("Seed concluído com sucesso.")
