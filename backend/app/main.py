from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.menu import router as menu_router
from app.routers.pedidos import router as pedidos_router
from app.routers.relatorios import router as relatorios_router

app = FastAPI(title="RESTAURANTE API", version="1.0.0")

app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(pedidos_router)
app.include_router(relatorios_router)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
