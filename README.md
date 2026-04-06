# RESTAURANTE 🍽️

Sistema de Gestão de Pedidos com backend FastAPI e frontend React.

## Estrutura

- `backend/` API REST, banco e testes.
- `frontend/` aplicação React (Vite).
- arquivos legados (`main.py`, `restaurante.py`, `pedido.py`) mantidos para referência CLI.

## Setup rápido

### Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python init_db.py
python seed.py
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Usuários de desenvolvimento

- `admin` / `admin123` (trocar em produção)
- `gerente` / `gerente123`
- `garcom` / `garcom123`
- `cozinha` / `cozinha123`

## Testes

```bash
cd backend
pytest tests/ -v
pytest tests/ -v --cov=app --cov-report=term-missing
```
