from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.Users import Users

class UsersRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Users | None:
        """Obtiene un usuario por su ID."""
        statement = select(Users).where(Users.id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> Users | None:
        """Obtiene un usuario por su correo electrónico."""
        statement = select(Users).where(Users.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_id_number(self, id_number: str) -> Users | None:
        """Obtiene un usuario por su número de identificación."""
        statement = select(Users).where(Users.id_number == id_number)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Users]:
        """Obtiene una lista paginada de todos los usuarios."""
        statement = select(Users).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, user: Users) -> Users:
        """Crea y persiste un nuevo usuario en la base de datos."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(
        self,
        user_id: int,
        name: str,
        lastname: str,
        address: str,
        zip_code: str,
        email: str,
        residence_city: str,
        country_id: int,
        cell_number: str,
        taxes: float,
        income: float,
        job: str,
        outcome: float,
        id_number: str,
        description: str,
    ) -> Users | None:
        db_user = self.get_by_id(user_id)
        if db_user:
            db_user.name = name
            db_user.lastname = lastname
            db_user.address = address
            db_user.zip_code = zip_code
            db_user.email = email
            db_user.residence_city = residence_city
            db_user.country_id = country_id
            db_user.cell_number = cell_number
            db_user.taxes = taxes
            db_user.income = income
            db_user.job = job
            db_user.outcome = outcome
            db_user.id_number = id_number
            db_user.description = description
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario."""
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
