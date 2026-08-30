# pyrefly: ignore [missing-import]
from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy import select
from Models.users import (
    UserLoginRequest, 
    UserLoginResponse, 
    UserLoginCreateSchema, 
    UserLoginDTO, 
    UserDTO, 
    UserRoleDTO,
    UserResponseSchema
)
from Services.IUsersLoginService import IUsersLoginService
from Repositories.IUsersLoginRepository import IUsersLoginRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Utils.security import hash_password, verify_password, create_access_token

class UsersLoginService(IUsersLoginService):
    """
    Servicio para el inicio de sesión y registro de credenciales de usuario.
    """
    def __init__(self, login_repository: IUsersLoginRepository, users_repository: IUsuariosRepository):
        self.login_repository = login_repository
        self.users_repository = users_repository

    def login(self, login_request: UserLoginRequest) -> UserLoginResponse:
        # 1. Obtener las credenciales por nombre de usuario
        db_login = self.login_repository.get_by_login(login_request.user_login)
        if not db_login:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nombre de usuario o contraseña incorrectos"
            )

        # 2. Verificar la contraseña
        if not verify_password(login_request.user_password, db_login.user_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nombre de usuario o contraseña incorrectos"
            )

        # 3. Obtener el perfil del usuario asociado
        user = self.users_repository.get_by_id(db_login.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de usuario asociado no encontrado"
            )

        # 4. Obtener el nombre del rol del usuario
        user.role = None
        if user.user_id_role:
            # Consultamos la tabla users_role usando la sesión de base de datos del repositorio
            db_session = getattr(self.users_repository, "db", None) or getattr(self.login_repository, "db", None)
            if db_session:
                role_statement = select(UserRoleDTO).where(UserRoleDTO.id == user.user_id_role)
                role_dto = db_session.execute(role_statement).scalar_one_or_none()
                if role_dto:
                    user.role = role_dto.role

        # 5. Generar token JWT
        token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(data=token_payload)

        # 6. Mapear y retornar la respuesta estructurada
        user_response = UserResponseSchema.model_validate(user)
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    def register_login(self, register_request: UserLoginCreateSchema) -> UserLoginDTO:
        # 1. Verificar si el usuario ya tiene credenciales registradas
        existing = self.login_repository.get_by_user_id(register_request.user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este usuario ya posee credenciales de inicio de sesión registradas"
            )

        # 2. Verificar si el nombre de usuario/login ya está en uso
        existing_login = self.login_repository.get_by_login(register_request.user_login)
        if existing_login:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario o correo de login ya está registrado"
            )

        # 3. Verificar que el perfil de usuario exista
        user = self.users_repository.get_by_id(register_request.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario especificado no existe"
            )

        # 4. Hashear la contraseña y guardar
        hashed_password = hash_password(register_request.user_password)
        login_dto = UserLoginDTO(
            user_id=register_request.user_id,
            user_login=register_request.user_login,
            user_password=hashed_password,
            active=True
        )

        return self.login_repository.create(login_dto)
