from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt

from app.auth import authenticate_user, create_access_token, get_current_user
from app.schemas.usuario import LoginRequest, LoginResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.login, data.senha)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": user["login"], "perfil": user["perfil"]})
    return {"access_token": token, "token_type": "bearer", "perfil": user["perfil"]}


@router.post("/logout")
def logout(_user=Depends(get_current_user)):
    return {"message": "Logout efetuado"}


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    data = dict(user)
    data.pop("senha_hash", None)
    data["senha_padrao_em_uso"] = bcrypt.verify("admin123", user["senha_hash"])
    return data
