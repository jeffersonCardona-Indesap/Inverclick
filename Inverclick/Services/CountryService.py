from Repositories.CountryRepository import CountryRepository
from Repositories.PrefixRepository import PrefixRepository  
from Models.Country import Country

class CountryService:

    def __init__(self, country_repository: CountryRepository, prefix_repository: PrefixRepository):
        self.country_repository = country_repository
        self.prefix_repository = prefix_repository

    def get_by_id(self, country_id: int) -> Country | None:
        country = self.country_repository.get_by_id(country_id)
        if country is None:
            raise ValueError(f"Country con ID {country_id} no encontrado.")
        return country

    def get_by_iso(self, iso: str) -> Country | None:
        country = self.country_repository.get_by_iso(iso)
        if country is None:
            raise ValueError(f"Country con código ISO {iso} no encontrado.")
        return country

    def get_by_name(self, name: str) -> Country | None:
        country = self.country_repository.get_by_name(name)
        if country is None:
            raise ValueError(f"Country con nombre {name} no encontrado.")
        return country

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Country]:
        return self.country_repository.get_all(skip, limit)

    def create(self, name: str, iso: str, prefix_id: int) -> Country:
        name = name.strip().title()
        iso = iso.strip().upper()

        existing_name = self.country_repository.get_by_name(name)
        if existing_name is not None:
            raise ValueError(f"Country con nombre {name} ya existe.")

        existing_iso = self.country_repository.get_by_iso(iso)
        if existing_iso is not None:
            raise ValueError(f"Country con código ISO {iso} ya existe.")

        existing_prefix = self.prefix_repository.get_by_id(prefix_id)
        if existing_prefix is None:
            raise ValueError(f"Prefix con ID {prefix_id} no encontrado.")

        new_country = Country(name=name, iso=iso, prefix_id=prefix_id)
        return self.country_repository.create(new_country)

    def update(self, country_id: int, name: str, iso: str, prefix_id: int) -> Country | None:
        name = name.strip().title()
        iso = iso.strip().upper()

        existing_name = self.country_repository.get_by_name(name)
        if existing_name is not None and existing_name.id != country_id:
            raise ValueError(f"Country con nombre {name} ya existe.")
        
        existing_iso = self.country_repository.get_by_iso(iso)
        if existing_iso is not None and existing_iso.id != country_id:
            raise ValueError(f"Country con código ISO {iso} ya existe.")

        existing_prefix = self.prefix_repository.get_by_id(prefix_id)
        if existing_prefix is None:
            raise ValueError(f"Prefix con ID {prefix_id} no encontrado.")

        updated_country = self.country_repository.update(country_id, name, iso, prefix_id)
        if updated_country is None:
            raise ValueError(f"Country con ID {country_id} no encontrado.")
        return updated_country

    def delete(self, country_id: int) -> None:
        deleted = self.country_repository.delete(country_id)
        if not deleted:
            raise ValueError(f"Country con ID {country_id} no encontrado.")
    