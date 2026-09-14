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

    def get_by_real_estate_id(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads asociados a una propiedad específica."""
        statement = (
            select(LeadDTO)
            .where(LeadDTO.id_real_state == real_estate_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

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

    def delete(self, lead_id: int) -> bool:
        """Elimina un lead por su ID."""
        db_lead = self.get_by_id(lead_id)
        if db_lead:
            self.db.delete(db_lead)
            self.db.commit()
            return True
        return False
