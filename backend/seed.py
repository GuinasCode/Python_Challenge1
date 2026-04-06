from passlib.hash import bcrypt

from app.database import DatabaseManager

MENU_ITEMS = [
    ("Frango Grelhado", 32.90),
    ("Filé ao Molho Madeira", 48.90),
    ("Massa ao Sugo", 28.50),
    ("Salmão ao Limão", 59.90),
    ("Risoto de Cogumelos", 42.00),
    ("Coca-Cola 350ml", 6.00),
    ("Suco Natural 500ml", 9.00),
    ("Água Mineral", 4.00),
    ("Petit Gateau", 18.00),
    ("Mousse de Maracujá", 14.00),
]


USERS = [
    ("gerente", "Gerente", "gerente@restaurante.com", "gerente123", "gerente"),
    ("garcom", "Garçom", "garcom@restaurante.com", "garcom123", "garcom"),
    ("cozinha", "Cozinha", "cozinha@restaurante.com", "cozinha123", "cozinha"),
]


def seed_menu():
    with DatabaseManager() as db:
        exists = db.execute_query("SELECT COUNT(1) AS total FROM menu")[0]["total"]
        if exists == 0:
            db.execute_many("INSERT INTO menu (item, valor) VALUES (?, ?)", MENU_ITEMS)


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
    seed_menu()
    create_admin()
    seed_users()


if __name__ == "__main__":
    seed()
    print("Seed concluído com sucesso.")
