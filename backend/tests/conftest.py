import os
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from passlib.hash import bcrypt

TEST_DB = Path(__file__).resolve().parent / "test_restaurante.db"
os.environ["RESTAURANTE_DB"] = str(TEST_DB)
os.environ["JWT_SECRET"] = "test-secret"

from app.main import app


@pytest.fixture(autouse=True)
def setup_db():
    if TEST_DB.exists():
        TEST_DB.unlink()
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.executescript(
        """
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
            perfil TEXT NOT NULL DEFAULT 'garcom',
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    cur.executemany(
        "INSERT INTO menu (item, valor) VALUES (?, ?)",
        [
            ("Frango Grelhado", 32.9),
            ("Massa ao Sugo", 28.5),
            ("Suco Natural 500ml", 9.0),
        ],
    )

    users = [
        ("admin", "Administrador", "admin@restaurante.com", bcrypt.hash("admin123"), "admin"),
        ("gerente", "Gerente", "gerente@restaurante.com", bcrypt.hash("gerente123"), "gerente"),
        ("garcom", "Garçom", "garcom@restaurante.com", bcrypt.hash("garcom123"), "garcom"),
        ("cozinha", "Cozinha", "cozinha@restaurante.com", bcrypt.hash("cozinha123"), "cozinha"),
    ]
    cur.executemany(
        "INSERT INTO users (login, nome, email, senha_hash, perfil) VALUES (?, ?, ?, ?, ?)",
        users,
    )
    conn.commit()
    conn.close()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture
def client():
    return TestClient(app)


def auth_header(client: TestClient, login: str, senha: str):
    response = client.post("/auth/login", json={"login": login, "senha": senha})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def gerente_headers(client):
    return auth_header(client, "gerente", "gerente123")


@pytest.fixture
def admin_headers(client):
    return auth_header(client, "admin", "admin123")


@pytest.fixture
def garcom_headers(client):
    return auth_header(client, "garcom", "garcom123")


@pytest.fixture
def cozinha_headers(client):
    return auth_header(client, "cozinha", "cozinha123")
