# Python_Challenge1 / RESTAURANTE

Este repositório começou como um desafio Python orientado a objetos para gerenciamento de pedidos em um restaurante.

Na branch do PR aberto (`#5`) ele evolui para uma aplicação web completa com:

- **backend FastAPI**
- **frontend React + Vite**
- **SQLite local**
- **seed inicial de usuários e cardápio**
- **testes com pytest**

> Os arquivos legados da versão CLI foram mantidos na raiz para compatibilidade, mas o fluxo principal desta branch está em `backend/` e `frontend/`.

## Estrutura

- `backend/` — API FastAPI, banco SQLite, autenticação e testes
- `frontend/` — interface web React/Vite
- `start-local.bat` — atalho para iniciar backend + frontend no Windows

## Requisitos

- **Python 3.10+** recomendado
  - Observação: `Python 3.7` não é suficiente para esta branch.
- **Node.js 20+**
- `npm`

## Instalação

### Backend

No Windows, se o `python` padrão apontar para uma versão antiga, use explicitamente um Python mais novo.

Exemplo com Python 3.12:

```bash
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se seu `python` local for 3.7, use outro executável, por exemplo:

```bash
C:\caminho\para\python312.exe -m venv .venv
```

### Frontend

```bash
cd frontend
npm install
```

## Inicialização do banco

Antes de subir a API pela primeira vez:

```bash
cd backend
.venv\Scripts\python.exe init_db.py
.venv\Scripts\python.exe seed.py
```

Isso cria o banco `backend/restaurante.db` e popula usuários e itens iniciais.

## Rodando localmente

### Opção 1: iniciar tudo com o script do Windows

Na raiz do projeto:

```bash
start-local.bat
```

### Opção 2: iniciar manualmente

#### Backend

```bash
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API: `http://localhost:8000`

#### Frontend

```bash
cd frontend
npm run dev
```

App web: `http://localhost:5173`

## Variáveis úteis

### Frontend

Você pode sobrescrever a URL da API criando `frontend/.env` a partir de `frontend/.env.example`:

```env
VITE_API_URL=http://localhost:8000
```

### Backend

Variáveis opcionais:

- `JWT_SECRET` — segredo JWT
- `RESTAURANTE_DB` — caminho alternativo para o SQLite
- `CORS_ALLOW_ORIGINS` — lista separada por vírgula de origens permitidas

Exemplo:

```bash
set JWT_SECRET=minha-chave-local
set CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Credenciais iniciais

Criadas pelo seed:

- `admin / admin123`
- `gerente / gerente123`
- `garcom / garcom123`
- `cozinha / cozinha123`

## Testes

```bash
cd backend
.venv\Scripts\python.exe -m pytest tests -q
```

## Endpoints principais

- `POST /auth/login`
- `GET /auth/me`
- `GET /menu`
- `POST /menu`
- `POST /pedidos`
- `GET /pedidos`
- `GET /pedidos/pendentes`
- `PATCH /pedidos/{id}/status`
- `GET /relatorios/receita`
- `GET /relatorios/itens-mais-vendidos`

Documentação interativa:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
