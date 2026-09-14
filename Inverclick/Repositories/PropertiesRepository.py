# pyrefly: ignore [missing-import]
from typing import Any
# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Models.real_estate import RealEstateDTO
from Repositories.IPropertiesRepository import IPropertiesRepository


class PropertiesRepository(IPropertiesRepository):
    """Implementación SQLAlchemy para el repositorio de propiedades (real_estate)."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, property_id: int) -> RealEstateDTO | None:
        """Obtiene una propiedad por su ID."""
        statement = select(RealEstateDTO).where(RealEstateDTO.id == property_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_name(self, name: str) -> RealEstateDTO | None:
        """Obtiene una propiedad por su nombre."""
        statement = select(RealEstateDTO).where(RealEstateDTO.name == name)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_address(self, address: str) -> RealEstateDTO | None:
        """Obtiene una propiedad por su dirección exacta."""
        statement = select(RealEstateDTO).where(RealEstateDTO.address == address)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_constructora_id(self, constructora_id: int, skip: int = 0, limit: int = 100) -> list[RealEstateDTO]:
        """Obtiene todas las propiedades de una constructora específica."""
        statement = (
            select(RealEstateDTO)
            .where(RealEstateDTO.id_constructionCompany == constructora_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RealEstateDTO]:
        """Obtiene una lista paginada de todas las propiedades."""
        statement = select(RealEstateDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, propertyDTO: RealEstateDTO) -> RealEstateDTO:
        """Crea y persiste una nueva propiedad en la base de datos."""
        self.db.add(propertyDTO)
        self.db.commit()
        self.db.refresh(propertyDTO)
        return propertyDTO

    def update(self, property_id: int, propertyDTO: RealEstateDTO | dict) -> RealEstateDTO | None:
        """Actualiza los datos de una propiedad existente."""
        db_property = self.get_by_id(property_id)
        if db_property:
            data = propertyDTO if isinstance(propertyDTO, dict) else {
                k: v for k, v in propertyDTO.__dict__.items() if not k.startswith('_')
            }
            for key, value in data.items():
                if value is not None and hasattr(db_property, key):
                    setattr(db_property, key, value)
            self.db.commit()
            self.db.refresh(db_property)
        return db_property

    def delete(self, property_id: int) -> bool:
        """Elimina una propiedad por su ID."""
        db_property = self.get_by_id(property_id)
        if db_property:
            self.db.delete(db_property)
            self.db.commit()
            return True
        return False
