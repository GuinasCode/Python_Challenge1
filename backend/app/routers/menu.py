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
    return MenuModel.create(data.item, data.valor)


@router.put("/{item_id}")
def update_menu_item(item_id: int, data: MenuIn, _user=Depends(require_roles("admin", "gerente"))):
    updated = MenuModel.update(item_id, data.item, data.valor)
    if not updated:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return updated


@router.delete("/{item_id}", status_code=204)
def delete_menu_item(item_id: int, _user=Depends(require_roles("admin", "gerente"))):
    if not MenuModel.delete(item_id):
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return Response(status_code=204)
