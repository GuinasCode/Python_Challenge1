from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    senha: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    perfil: str


class UserOut(BaseModel):
    id: int
    login: str
    nome: str
    email: str
    perfil: str
    ativo: int
    criado_em: str
    senha_padrao_em_uso: bool = False
