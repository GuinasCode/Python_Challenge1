from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import get_current_user, require_roles
from app.models.pedido import Order
from app.schemas.pedido import PedidoCreate

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("")
def list_pedidos(data: str | None = None, status: str | None = None, _user=Depends(get_current_user)):
    return Order.list_all(data=data, status_filter=status)


@router.get("/pendentes")
def list_pendentes(_user=Depends(get_current_user)):
    return Order.list_pending()


@router.get("/{pedido_id}")
def get_pedido(pedido_id: int, _user=Depends(get_current_user)):
    pedido = Order.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.post("", status_code=201)
def create_pedido(data: PedidoCreate, _user=Depends(require_roles("garcom", "admin", "gerente"))):
    try:
        return Order.create(data.nome_cliente, data.itens)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/{pedido_id}/status")
def advance_pedido_status(pedido_id: int, user=Depends(get_current_user)):
    pedido = Order.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    perfil = user["perfil"]
    atual = pedido["status"]
    if atual == "Pendente" and perfil not in {"admin", "gerente", "cozinha"}:
        raise HTTPException(status_code=403, detail="Sem permissão para iniciar preparo")
    if atual == "Em preparo" and perfil not in {"admin", "gerente", "cozinha"}:
        raise HTTPException(status_code=403, detail="Sem permissão para marcar como pronto")
    if atual == "Pronto" and perfil not in {"admin", "gerente", "garcom"}:
        raise HTTPException(status_code=403, detail="Sem permissão para entregar")

    try:
        return Order.advance_status(pedido_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{pedido_id}", status_code=204)
def cancel_pedido(pedido_id: int, _user=Depends(require_roles("admin", "gerente"))):
    try:
        Order.delete(pedido_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Response(status_code=204)
