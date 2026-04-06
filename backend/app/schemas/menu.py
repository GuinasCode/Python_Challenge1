from pydantic import BaseModel, Field


class MenuIn(BaseModel):
    item: str = Field(min_length=2)
    valor: float = Field(gt=0)


class MenuOut(MenuIn):
    id: int
