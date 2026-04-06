import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt

from app.models.usuario import UserModel

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(login: str, senha: str):
    user = UserModel.get_by_login(login)
    if not user or not user["ativo"]:
        return None
    if not verify_password(senha, user["senha_hash"]):
        return None
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        if not login:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = UserModel.get_by_login(login)
    if not user:
        raise credentials_exception
    return user


def require_roles(*roles: str):
    def _checker(user=Depends(get_current_user)):
        if user["perfil"] not in roles:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return user

    return _checker
