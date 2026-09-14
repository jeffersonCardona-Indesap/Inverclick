from Models.constructoras import ConstructionCompanyDTO


class IConstructorasRepository:
    """
    Interfaz para el repositorio de constructoras.
    """
    def get_by_id(self, company_id: int) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su ID."""
        pass

    def get_by_nit(self, nit: str) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su NIT."""
        pass

    def get_by_nombre(self, nombre: str) -> ConstructionCompanyDTO | None:
        """Obtiene una constructora por su nombre."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ConstructionCompanyDTO]:
        """Obtiene una lista paginada de todas las constructoras."""
        pass

    def create(self, companyDTO: ConstructionCompanyDTO) -> ConstructionCompanyDTO:
        """Crea y persiste una nueva constructora en la base de datos."""
        pass

    def update(self, company_id: int, companyDTO: ConstructionCompanyDTO | dict) -> ConstructionCompanyDTO | None:
        """Actualiza los datos de una constructora existente."""
        pass

    def delete(self, company_id: int) -> bool:
        """Elimina una constructora por su ID."""
        pass
