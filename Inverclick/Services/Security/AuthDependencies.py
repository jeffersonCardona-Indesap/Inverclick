from typing import Callable, Optional, Any
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from Services.Security.JwtService import decode_access_token

# Configuración del esquema OAuth2 Password Bearer para Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users-login/login", auto_error=False)

def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> dict[str, Any]:
    """
    Dependencia para obtener y validar la información del usuario autenticado desde el token JWT.
    """
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token de sesión no proporcionado. Debe autenticarse para realizar esta operación."
        )
    return decode_access_token(token)

def require_module(required_module: str) -> Callable[..., dict[str, Any]]:
    """
    Fábrica de dependencias de autorización basada en roles y módulos (RBAC).
    Permite el acceso si:
    - El rol del usuario es Master o su lista de módulos incluye "All".
    - El módulo requerido está presente en la lista de módulos del usuario.
    """
    def permission_checker(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        role = str(current_user.get("role", "")).strip()
        raw_modules = current_user.get("modules", []) or []
        user_modules = [str(m).strip().lower() for m in raw_modules]

        # El rol Master o la presencia del módulo 'All' otorga acceso total a todos los endpoints
        if role.lower() == "master" or "all" in user_modules:
            return current_user

        # Verificar si el módulo requerido coincide con los módulos asignados al usuario
        if required_module.strip().lower() in user_modules:
            return current_user

        raise HTTPException(
            status_code=403,
            detail=f"Acceso denegado. El rol '{role}' no tiene permisos para operar en el módulo '{required_module}'."
        )

    return permission_checker
