from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.Prefix import Prefix

class PrefixRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, prefix_id: int) -> Prefix | None:
        """Obtiene un Prefix por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(Prefix).where(Prefix.id == prefix_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_code(self, code: str) -> Prefix | None:
        """Obtiene un Prefix por su código."""
        statement = select(Prefix).where(Prefix.code == code)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        """Obtiene una lista paginada de todos los Prefixs."""
        statement = select(Prefix).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, prefix: Prefix) -> Prefix:
        """Crea y persiste un nuevo Prefix en la base de datos."""
        self.db.add(prefix)
        self.db.commit()
        self.db.refresh(prefix)
        return prefix

    def update(self, prefix_id: int, code: str) -> Prefix | None:
        """Actualiza los datos de un Prefix existente."""
        db_prefix = self.get_by_id(prefix_id)
        if db_prefix:
            db_prefix.code = code
            self.db.commit()
            self.db.refresh(db_prefix)
        return db_prefix

    def delete(self, prefix_id: int) -> bool:
        """Elimina un Prefix."""
        db_prefix = self.get_by_id(prefix_id)
        if db_prefix:
            self.db.delete(db_prefix)
            self.db.commit()
            return True
        return False
