from pydantic import BaseModel, Field


class MenuIn(BaseModel):
    item: str = Field(min_length=2)
    valor: float = Field(gt=0)
    categoria_id: int | None = Field(default=None, gt=0)
    imagem_base64: str | None = None


class MenuOut(MenuIn):
    id: int
    categoria_nome: str | None = None
    categoria_ordem: int | None = None
