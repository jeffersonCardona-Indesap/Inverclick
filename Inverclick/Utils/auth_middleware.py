# pyrefly: ignore [missing-import]
from fastapi import Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from sqlalchemy import select
from Repositories.database import get_db
from Models.users import UserDTO, UserRoleDTO
from Utils.security import decode_access_token

# Esquema de seguridad Bearer
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserDTO:
    """
    Dependencia para obtener el usuario actual a partir del token JWT Bearer.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extraer el ID de usuario del payload (sub)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token con formato incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buscar el usuario en la base de datos
    statement = select(UserDTO).where(UserDTO.id == int(user_id))
    user = db.execute(statement).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener el rol del usuario si existe
    user.role = None
    if user.user_id_role:
        role_statement = select(UserRoleDTO).where(UserRoleDTO.id == user.user_id_role)
        role_dto = db.execute(role_statement).scalar_one_or_none()
        if role_dto:
            user.role = role_dto.role
            
    return user

class RoleChecker:
    """
    Clase para comprobar si el usuario actual posee alguno de los roles permitidos.
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserDTO = Depends(get_current_user)) -> UserDTO:
        if not current_user.role or current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere uno de los siguientes roles: {', '.join(self.allowed_roles)}",
            )
        return current_user
