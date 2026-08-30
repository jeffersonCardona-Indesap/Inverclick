# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Models.users import UserLoginDTO
from Repositories.IUsersLoginRepository import IUsersLoginRepository

class UsersLoginRepository(IUsersLoginRepository):
    """
    Implementación en SQLAlchemy para el repositorio de inicio de sesión.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_by_login(self, user_login: str) -> UserLoginDTO | None:
        """Obtiene una credencial activa por su nombre de usuario/login."""
        statement = select(UserLoginDTO).where(UserLoginDTO.user_login == user_login, UserLoginDTO.active == True)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        """Obtiene una credencial de inicio de sesión por el ID de usuario."""
        statement = select(UserLoginDTO).where(UserLoginDTO.user_id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def create(self, loginDTO: UserLoginDTO) -> UserLoginDTO:
        """Persiste una nueva credencial en la base de datos."""
        self.db.add(loginDTO)
        self.db.commit()
        self.db.refresh(loginDTO)
        return loginDTO
