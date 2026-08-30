# pyrefly: ignore [missing-import]
from Models.users import UserLoginDTO

class IUsersLoginRepository:
    """
    Interfaz para el repositorio de inicio de sesión de usuarios (users_login).
    """
    def get_by_login(self, user_login: str) -> UserLoginDTO | None:
        """Obtiene una credencial de inicio de sesión por su nombre de usuario/login."""
        pass

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        """Obtiene una credencial de inicio de sesión por su ID de usuario asociado."""
        pass

    def create(self, loginDTO: UserLoginDTO) -> UserLoginDTO:
        """Crea y persiste un nuevo inicio de sesión en la base de datos."""
        pass
