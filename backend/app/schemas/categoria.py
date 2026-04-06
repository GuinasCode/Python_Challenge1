from pydantic import BaseModel, Field


class CategoriaIn(BaseModel):
    nome: str = Field(min_length=2, max_length=60)
    ordem: int = Field(default=0, ge=0, le=999)


class CategoriaOut(CategoriaIn):
    id: int
    total_itens: int = 0
