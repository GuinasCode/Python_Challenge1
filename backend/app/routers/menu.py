from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import get_current_user, require_roles
from app.models.menu import MenuModel
from app.schemas.menu import MenuIn

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("")
def list_menu(_user=Depends(get_current_user)):
    return MenuModel.list_all()


@router.post("", status_code=201)
def create_menu_item(data: MenuIn, _user=Depends(require_roles("admin", "gerente"))):
    try:
        return MenuModel.create(**data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/{item_id}")
def update_menu_item(item_id: int, data: MenuIn, _user=Depends(require_roles("admin", "gerente"))):
    try:
        updated = MenuModel.update(item_id, **data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return updated


@router.delete("/{item_id}", status_code=204)
def delete_menu_item(item_id: int, _user=Depends(require_roles("admin", "gerente"))):
    if not MenuModel.delete(item_id):
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return Response(status_code=204)
