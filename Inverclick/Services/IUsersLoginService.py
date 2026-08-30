# pyrefly: ignore [missing-import]
from Models.users import UserLoginRequest, UserLoginResponse, UserLoginCreateSchema, UserLoginDTO

class IUsersLoginService:
    """
    Interfaz para el servicio de inicio de sesión y autenticación.
    """
    def login(self, login_request: UserLoginRequest) -> UserLoginResponse:
        """Autentica a un usuario y genera su token JWT."""
        pass

    def register_login(self, register_request: UserLoginCreateSchema) -> UserLoginDTO:
        """Registra credenciales de acceso (hasheadas) para un usuario existente."""
        pass
