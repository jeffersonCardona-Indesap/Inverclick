from Models.real_estate import RealEstateDTO


class IPropertiesRepository:
    """
    Interfaz para el repositorio de propiedades (real_estate).
    """
    def get_by_id(self, property_id: int) -> RealEstateDTO | None:
        """Obtiene una propiedad por su ID."""
        pass

    def get_by_name(self, name: str) -> RealEstateDTO | None:
        """Obtiene una propiedad por su nombre."""
        pass

    def get_by_address(self, address: str) -> RealEstateDTO | None:
        """Obtiene una propiedad por su dirección."""
        pass

    def get_by_constructora_id(self, constructora_id: int, skip: int = 0, limit: int = 100) -> list[RealEstateDTO]:
        """Obtiene todas las propiedades de una constructora específica."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RealEstateDTO]:
        """Obtiene una lista paginada de todas las propiedades."""
        pass

    def create(self, propertyDTO: RealEstateDTO) -> RealEstateDTO:
        """Crea y persiste una nueva propiedad en la base de datos."""
        pass

    def update(self, property_id: int, propertyDTO: RealEstateDTO | dict) -> RealEstateDTO | None:
        """Actualiza los datos de una propiedad existente."""
        pass

    def delete(self, property_id: int) -> bool:
        """Elimina una propiedad por su ID."""
        pass
