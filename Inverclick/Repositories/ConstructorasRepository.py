# pyrefly: ignore [missing-import]
from typing import Any
# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Models.constructoras import ConstructionCompanyDTO
from Repositories.IConstructorasRepository import IConstructorasRepository


class ConstructorasRepository(IConstructorasRepository):
    """Implementación SQLAlchemy para el repositorio de constructoras."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, company_id: int) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su ID."""
        statement = select(ConstructionCompanyDTO).where(ConstructionCompanyDTO.id == company_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_nit(self, nit: str) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su NIT."""
        statement = select(ConstructionCompanyDTO).where(ConstructionCompanyDTO.nit == nit)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_nombre(self, nombre: str) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su nombre."""
        statement = select(ConstructionCompanyDTO).where(ConstructionCompanyDTO.Nombre == nombre)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ConstructionCompanyDTO]:
        """Obtiene una lista paginada de todas las constructoras."""
        statement = select(ConstructionCompanyDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, companyDTO: ConstructionCompanyDTO) -> ConstructionCompanyDTO:
        """Crea y persiste una nueva constructora en la base de datos."""
        self.db.add(companyDTO)
        self.db.commit()
        self.db.refresh(companyDTO)
        return companyDTO

    def update(self, company_id: int, companyDTO: ConstructionCompanyDTO | dict) -> ConstructionCompanyDTO | None:
        """Actualiza los datos de una constructora existente."""
        db_company = self.get_by_id(company_id)
        if db_company:
            data = companyDTO if isinstance(companyDTO, dict) else {
                k: v for k, v in companyDTO.__dict__.items() if not k.startswith('_')
            }
            for key, value in data.items():
                if value is not None and hasattr(db_company, key):
                    setattr(db_company, key, value)
            self.db.commit()
            self.db.refresh(db_company)
        return db_company

    def delete(self, company_id: int) -> bool:
        """Elimina una constructora por su ID."""
        db_company = self.get_by_id(company_id)
        if db_company:
            self.db.delete(db_company)
            self.db.commit()
            return True
        return False
