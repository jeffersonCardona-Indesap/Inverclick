from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Services.IUsersLoginService import IUsersLoginService
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Services.Impl.UsersLoginService import UsersLoginService
from Utils.HttpResponses.userLoginHttpResponses import UserLoginHttpResponses
from Utils.user_login_validator import UserLoginValidator
from Repositories.database import get_db
from Services.Security.AuthDependencies import require_module
from Models.users_login import (
    UserLoginDTO, 
    LoginRequestSchema, 
    UserLoginCreateSchema, 
    UserLoginUpdateSchema, 
    UserLoginResponseSchema,
    TokenResponseSchema
)

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/users-login", tags=["UsersLogin"])

# Dependencia para resolver e instanciar el servicio de login de usuarios
def get_users_login_service(db: Session = Depends(get_db)) -> IUsersLoginService:
    repository = UsersLoginRepository(db)
    users_repository = UsersRepository(db)
    users_role_repository = UsersRoleRepository(db)
    http_responses = UserLoginHttpResponses()
    validator = UserLoginValidator()
    return UsersLoginService(
        repository=repository, 
        http_responses=http_responses, 
        validator=validator, 
        users_repository=users_repository,
        users_role_repository=users_role_repository
    )

# --- Endpoint Público de Autenticación / Login ---

@router.post(
    "/login", 
    response_model=TokenResponseSchema,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": LoginRequestSchema.model_json_schema()
                },
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "description": "user_login o nombre de usuario"},
                            "password": {"type": "string", "description": "Contraseña de usuario"},
                            "user_login": {"type": "string"},
                            "user_password": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
)
async def login(
    request: Request,
    service: IUsersLoginService = Depends(get_users_login_service)
):
    """
    Endpoint para autenticación de usuarios por user_login y contraseña.
    Genera un token de sesión JWT con expiración de 5 minutos (parametrizable en .env).
    Soporta JSON body (user_login, user_password) y Form Data de Swagger UI Authorize (username, password).
    """
    user_login = ""
    user_password = ""

    content_type = request.headers.get("content-type", "")
    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        user_login = str(form.get("username") or form.get("user_login") or "").strip()
        user_password = str(form.get("password") or form.get("user_password") or "").strip()
    else:
        try:
            body = await request.json()
            user_login = str(body.get("user_login") or body.get("username") or "").strip()
            user_password = str(body.get("user_password") or body.get("password") or "").strip()
        except Exception:
            pass

    return service.authenticate_and_get_token(user_login, user_password)

# --- Endpoints Protegidos por Sesión / Módulo Usuarios ---

@router.get("/{login_id}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("Usuarios"))])
def get_login_by_id(login_id: int, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_by_id(login_id)

@router.get("/user/{user_id}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("Usuarios"))])
def get_login_by_user_id(user_id: int, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_by_user_id(user_id)

@router.get("/login/{user_login}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("Usuarios"))])
def get_login_by_user_login(user_login: str, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_by_user_login(user_login)

@router.get("", response_model=list[UserLoginResponseSchema], dependencies=[Depends(require_module("Usuarios"))])
def get_all_logins(skip: int = 0, limit: int = 100, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_all(skip=skip, limit=limit)

@router.post("", status_code=201, response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("Usuarios"))])
def create_login(login: UserLoginCreateSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    login_dto = UserLoginDTO(**login.model_dump(exclude_none=True))
    return service.create(login_dto)

@router.put("/{login_id}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("Usuarios"))])
def update_login(login_id: int, login: UserLoginUpdateSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    login_dto = UserLoginDTO(**login.model_dump(exclude_unset=True))
    return service.update(login_id, login_dto)

@router.delete("/{login_id}", dependencies=[Depends(require_module("Usuarios"))])
def delete_login(login_id: int, service: IUsersLoginService = Depends(get_users_login_service)):
    return {"success": service.delete(login_id)}
