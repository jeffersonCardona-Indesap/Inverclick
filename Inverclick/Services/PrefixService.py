from Repositories.PrefixRepository import PrefixRepository
from Models.Prefix import Prefix

class PrefixService:

    def __init__(self, prefix_repository: PrefixRepository):
        self.prefix_repository = prefix_repository

    def get_by_id(self, prefix_id: int) -> Prefix | None:
        prefix =  self.prefix_repository.get_by_id(prefix_id)
        if prefix is None:
            raise ValueError(f"Prefix con ID {prefix_id} no encontrado.")
        return prefix

    def get_by_code(self, code: str) -> Prefix | None:
        prefix = self.prefix_repository.get_by_code(code)
        if prefix is None:
            raise ValueError(f"Prefijo {code} no encontrado.")
        return prefix

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        return self.prefix_repository.get_all(skip, limit)

    def create(self, code: str) -> Prefix:
        existing_prefix = self.prefix_repository.get_by_code(code)
        if existing_prefix is not None:
            raise ValueError(f"Prefix con prefijo {code} ya existe.")

        new_prefix = Prefix(code=code)
        return self.prefix_repository.create(new_prefix)

    def update(self, prefix_id: int, code: str) -> Prefix | None:
        existing_prefix = self.prefix_repository.get_by_code(code)
        if existing_prefix is not None and existing_prefix.id != prefix_id:
            raise ValueError(f"Prefijo {code} ya existe.")

        updated_prefix = self.prefix_repository.update(prefix_id, code)
        if updated_prefix is None:
            raise ValueError(f"Prefix con ID {prefix_id} no encontrado.")
        return updated_prefix

    def delete(self, prefix_id: int) -> None:
        deleted = self.prefix_repository.delete(prefix_id)
        if not deleted:
            raise ValueError(f"Prefix con ID {prefix_id} no encontrado.")
