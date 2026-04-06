from fastapi import APIRouter, Depends

from app.auth import require_roles
from app.models.pedido import Order

router = APIRouter(prefix="/relatorios", tags=["relatorios"])


@router.get("/receita")
def get_receita(inicio: str | None = None, fim: str | None = None, _user=Depends(require_roles("admin", "gerente"))):
    return Order.revenue(inicio=inicio, fim=fim)


@router.get("/itens-mais-vendidos")
def itens_mais_vendidos(_user=Depends(require_roles("admin", "gerente"))):
    return Order.best_sellers()
