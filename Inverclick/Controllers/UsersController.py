# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from Services.IUsuariosService import IUsuariosService
# pyrefly: ignore [missing-import]
from Services.Impl.UsuariosService import UsuariosService
# pyrefly: ignore [missing-import]
from Repositories.UsersRepository import UsersRepository
# pyrefly: ignore [missing-import]
from Repositories.PrefixRepository import PrefixRepository
# pyrefly: ignore [missing-import]
from Utils.HttpResponses.userHttpResponses import UserHttpResponses
# pyrefly: ignore [missing-import]
from Utils.user_validator import UserValidator
# pyrefly: ignore [missing-import]
from Repositories.database import get_db
# pyrefly: ignore [missing-import]
from Repositories.ConstructorasRepository import ConstructorasRepository
from Models.users import UserDTO, UserCreateSchema, UserUpdateSchema, UserResponseSchema
from Utils.auth_middleware import RoleChecker

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/users", tags=["Users"])

role_master_or_admin = RoleChecker(["Master", "Admin"])
role_master_only = RoleChecker(["Master"])

# Dependencia para resolver e instanciar el servicio de usuarios
def get_usuarios_service(db: Session = Depends(get_db)) -> IUsuariosService:
    repository = UsersRepository(db)
    prefix_repository = PrefixRepository(db)
    constructoras_repository = ConstructorasRepository(db)
    http_responses = UserHttpResponses()
    validator = UserValidator()
    return UsuariosService(repository, prefix_repository, http_responses, validator, constructoras_repository)

# --- Endpoints del API ---

@router.get("/{usuario_id}", response_model=UserResponseSchema)
def get_user_by_id(
    usuario_id: int, 
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_or_admin)
):
    return service.get_by_id(usuario_id)

@router.get("/email/{email}", response_model=UserResponseSchema)
def get_user_by_email(
    email: str, 
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_or_admin)
):
    return service.get_by_email(email)

@router.get("", response_model=list[UserResponseSchema])
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_or_admin)
):
    return service.get_all(skip=skip, limit=limit)

@router.post("", status_code=201, response_model=UserResponseSchema)
def create_user(
    user: UserCreateSchema, 
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_or_admin)
):
    user_dto = UserDTO(**user.model_dump(exclude_none=True))
    return service.create(user_dto)

@router.put("/{usuario_id}", response_model=UserResponseSchema)
def update_user(
    usuario_id: int, 
    user: UserUpdateSchema, 
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_or_admin)
):
    user_dto = UserDTO(**user.model_dump(exclude_unset=True))
    return service.update(user_id=usuario_id, userDTO=user_dto)

@router.put("/{usuario_id}/assign-constructora/{constructora_id}", response_model=UserResponseSchema)
def assign_constructora_to_user(
    usuario_id: int,
    constructora_id: int,
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_only)
):
    """Asigna una constructora a un usuario con rol Constructora (solo Master)."""
    return service.assign_constructora(user_id=usuario_id, constructora_id=constructora_id)

@router.delete("/{usuario_id}")
def delete_user(
    usuario_id: int, 
    service: IUsuariosService = Depends(get_usuarios_service),
    current_user: UserDTO = Depends(role_master_only)
):
    return {"success": service.delete(usuario_id)}