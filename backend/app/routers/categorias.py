from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import get_current_user, require_roles
from app.models.categoria import CategoryModel
from app.schemas.categoria import CategoriaIn

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("")
def list_categories(_user=Depends(get_current_user)):
    return CategoryModel.list_all()


@router.post("", status_code=201)
def create_category(data: CategoriaIn, _user=Depends(require_roles("admin", "gerente"))):
    try:
        return CategoryModel.create(data.nome, data.ordem)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/{category_id}")
def update_category(category_id: int, data: CategoriaIn, _user=Depends(require_roles("admin", "gerente"))):
    try:
        updated = CategoryModel.update(category_id, data.nome, data.ordem)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return updated


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, _user=Depends(require_roles("admin", "gerente"))):
    try:
        deleted = CategoryModel.delete(category_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return Response(status_code=204)
