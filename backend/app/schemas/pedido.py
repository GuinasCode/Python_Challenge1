from pydantic import BaseModel, Field, field_validator


class PedidoItemIn(BaseModel):
    item_id: int = Field(gt=0)
    quantidade: int = Field(default=1, gt=0)


class PedidoCreate(BaseModel):
    nome_cliente: str = Field(min_length=2)
    itens: list[PedidoItemIn] = Field(min_length=1)

    @field_validator("itens", mode="before")
    @classmethod
    def normalize_itens(cls, value):
        if not isinstance(value, list):
            return value

        normalized = []
        for item in value:
            if isinstance(item, int):
                normalized.append({"item_id": item, "quantidade": 1})
            elif isinstance(item, dict) and "item_id" not in item and "id" in item:
                normalized.append({**item, "item_id": item["id"]})
            else:
                normalized.append(item)
        return normalized


class PedidoItemDetalhadoOut(BaseModel):
    item_id: int | None = None
    nome: str
    quantidade: int
    valor_unitario: float
    subtotal: float
    categoria_id: int | None = None
    categoria_nome: str | None = None
    imagem_base64: str | None = None


class PedidoOut(BaseModel):
    id: int
    data: str
    nome_cliente: str
    itens: str
    status: str
    valor_total: float
    itens_detalhados: list[PedidoItemDetalhadoOut] = []


class ReceitaOut(BaseModel):
    total: float
    inicio: str
    fim: str
