from typing import Any
from Models.constructoras import ConstructionCompanyDTO


class IConstructorasService:
    """
    Interfaz para el servicio de constructoras.
    """
    def get_by_id(self, company_id: int) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su ID."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ConstructionCompanyDTO]:
        """Obtiene una lista paginada de todas las constructoras."""
        pass

    def create(self, companyDTO: ConstructionCompanyDTO) -> ConstructionCompanyDTO:
        """Crea y persiste una nueva constructora."""
        pass

    def update(self, company_id: int, companyDTO: ConstructionCompanyDTO) -> ConstructionCompanyDTO | None:
        """Actualiza los datos de una constructora existente."""
        pass

    def delete(self, company_id: int) -> bool:
        """Elimina una constructora por su ID."""
        pass
