# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Models.users import UserLoginRequest, UserLoginResponse, UserLoginCreateSchema
from Services.IUsersLoginService import IUsersLoginService
from Services.Impl.UsersLoginService import UsersLoginService
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsersRepository import UsersRepository

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_service(db: Session = Depends(get_db)) -> IUsersLoginService:
    login_repository = UsersLoginRepository(db)
    users_repository = UsersRepository(db)
    return UsersLoginService(login_repository, users_repository)

@router.post("/login", response_model=UserLoginResponse)
def login(
    login_request: UserLoginRequest, 
    service: IUsersLoginService = Depends(get_auth_service)
):
    """
    Endpoint para autenticación de usuarios. Retorna el token JWT y los datos del usuario.
    """
    return service.login(login_request)

@router.post("/register-login", status_code=status.HTTP_201_CREATED)
def register_login(
    register_request: UserLoginCreateSchema, 
    service: IUsersLoginService = Depends(get_auth_service)
):
    """
    Endpoint para registrar credenciales de acceso para un perfil de usuario existente.
    """
    service.register_login(register_request)
    return {"message": "Credenciales de inicio de sesión creadas exitosamente"}
