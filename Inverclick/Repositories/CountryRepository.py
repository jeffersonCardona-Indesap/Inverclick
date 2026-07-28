from sqlalchemy import select, func
from sqlalchemy.orm import Session
from Models.Country import Country

class CountryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, country_id: int) -> Country | None:
        """Obtiene un Country por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(Country).where(Country.id == country_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_iso(self, iso: str) -> Country | None:
        """Obtiene un Country por su código ISO."""
        statement = select(Country).where(func.lower(Country.iso) == func.lower(iso))
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_name(self, name: str) -> Country | None:
        """Obtiene un Country por su nombre."""
        statement = select(Country).where(func.lower(Country.name) == func.lower(name))
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Country]:
        """Obtiene una lista paginada de todos los Countries."""
        statement = select(Country).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, country: Country) -> Country:
        """Crea y persiste un nuevo Country en la base de datos."""
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)
        return country

    def update(self, country_id: int, name: str, iso: str, prefix_id: int) -> Country | None:
        """Actualiza los datos de un Country existente."""
        db_country = self.get_by_id(country_id)
        if db_country:
            db_country.name = name
            db_country.iso = iso
            db_country.prefix_id = prefix_id
            self.db.commit()
            self.db.refresh(db_country)
        return db_country

    def delete(self, country_id: int) -> bool:
        """Elimina un Country."""
        db_country = self.get_by_id(country_id)
        if db_country:
            self.db.delete(db_country)
            self.db.commit()
            return True
        return False