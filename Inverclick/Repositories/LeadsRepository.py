# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Models.leads import LeadDTO
from Repositories.ILeadsRepository import ILeadsRepository


class LeadsRepository(ILeadsRepository):
    """Implementación SQLAlchemy para el repositorio de leads."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        """Obtiene un lead por su ID."""
        statement = select(LeadDTO).where(LeadDTO.id == lead_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads de un usuario específico."""
        statement = (
            select(LeadDTO)
            .where(LeadDTO.id_user == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def get_favorites_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads activos marcados como favoritos por un usuario específico."""
        statement = (
            select(LeadDTO)
            .where(LeadDTO.id_user == user_id, LeadDTO.is_favorite == True)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def get_by_real_estate_id(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads asociados a una propiedad específica."""
        statement = (
            select(LeadDTO)
            .where(LeadDTO.id_real_state == real_estate_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def get_by_constructora_id(self, constructora_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads asociados a una constructora específica."""
        statement = (
            select(LeadDTO)
            .where(LeadDTO.id_constructionCompany == constructora_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def get_by_user_and_target(self, user_id: int, real_estate_id: int | None = None, constructora_id: int | None = None) -> LeadDTO | None:
        """Busca un lead existente por usuario y propiedad o constructora objetivo."""
        stmt = select(LeadDTO).where(LeadDTO.id_user == user_id)
        if real_estate_id is not None:
            stmt = stmt.where(LeadDTO.id_real_state == real_estate_id)
        elif constructora_id is not None:
            stmt = stmt.where(LeadDTO.id_constructionCompany == constructora_id, LeadDTO.id_real_state.is_(None))
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene una lista paginada de todos los leads."""
        statement = select(LeadDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, leadDTO: LeadDTO) -> LeadDTO:
        """Crea y persiste un nuevo lead en la base de datos."""
        self.db.add(leadDTO)
        self.db.commit()
        self.db.refresh(leadDTO)
        return leadDTO

    def update(self, lead_id: int, data: dict) -> LeadDTO | None:
        """Actualiza los datos de un lead."""
        db_lead = self.get_by_id(lead_id)
        if db_lead:
            for key, value in data.items():
                if hasattr(db_lead, key):
                    setattr(db_lead, key, value)
            self.db.commit()
            self.db.refresh(db_lead)
        return db_lead

    def delete(self, lead_id: int) -> bool:
        """Elimina un lead por su ID."""
        db_lead = self.get_by_id(lead_id)
        if db_lead:
            self.db.delete(db_lead)
            self.db.commit()
            return True
        return False

