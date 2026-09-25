import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "inverclick_jwt_secret_session_key_2026_secure")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "5"))

def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> tuple[str, int]:
    """
    Crea un token JWT de sesión con el payload especificado y tiempo de expiración.
    Retorna la tupla (token_str, expires_in_seconds).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        expires_in = int(expires_delta.total_seconds())
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
        expires_in = EXPIRE_MINUTES * 60

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expires_in

def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decodifica y valida un token JWT de sesión.
    Si expiró o es inválido, lanza HTTPException 401.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token de sesión ha expirado. Por favor, vuelva a iniciar sesión."
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Token de sesión inválido o alterado."
        )
