from pydantic import BaseModel, Field


class PedidoCreate(BaseModel):
    nome_cliente: str = Field(min_length=2)
    itens: list[int] = Field(min_length=1)


class PedidoOut(BaseModel):
    id: int
    data: str
    nome_cliente: str
    itens: str
    status: str
    valor_total: float


class ReceitaOut(BaseModel):
    total: float
    inicio: str
    fim: str
