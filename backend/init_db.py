import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "restaurante.db"


def create_tables():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.executescript(
        '''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            nome_cliente TEXT NOT NULL,
            itens TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            valor_total REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            valor REAL NOT NULL
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
        '''
    )

    connection.commit()
    connection.close()


if __name__ == '__main__':
    create_tables()
    print(f'Banco de dados e tabelas inicializados com sucesso em: {DB_PATH}')
