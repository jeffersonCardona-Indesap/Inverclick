# pyrefly: ignore [missing-import]
from Models.prefix import Prefix

class IPrefixService:
    """
    Interfaz para el servicio de prefijos.
    """
    def get_by_id(self, prefix_id: int) -> Prefix | None:
        pass

    def get_by_prefix(self, prefix: str) -> Prefix | None:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        pass


