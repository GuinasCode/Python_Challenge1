import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.categoria import CategoryModel
from app.routers.auth import router as auth_router
from app.routers.categorias import router as categorias_router
from app.routers.menu import router as menu_router
from app.routers.pedidos import router as pedidos_router
from app.routers.relatorios import router as relatorios_router


def get_allowed_origins() -> list[str]:
    configured = os.getenv("CORS_ALLOW_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]


app = FastAPI(title="RESTAURANTE API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(menu_router)
app.include_router(pedidos_router)
app.include_router(relatorios_router)


@app.on_event("startup")
def ensure_reference_data():
    CategoryModel.ensure_defaults()


@app.get("/")
def healthcheck():
    return {"status": "ok"}
