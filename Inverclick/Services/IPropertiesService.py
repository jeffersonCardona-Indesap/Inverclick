from typing import Any
from Models.real_estate import RealEstateDTO
from Models.users import UserDTO


class IPropertiesService:
    """
    Interfaz para el servicio de propiedades (real_estate).
    """
    def get_by_id(self, property_id: int, current_user: UserDTO | None = None) -> RealEstateDTO | None:
        """Obtiene una propiedad por su ID."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[RealEstateDTO]:
        """Obtiene una lista paginada de todas las propiedades."""
        pass

    def get_by_constructora(self, constructora_id: int, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[RealEstateDTO]:
        """Obtiene las propiedades de una constructora específica."""
        pass

    def create(self, propertyDTO: RealEstateDTO, current_user: UserDTO | None = None) -> RealEstateDTO:
        """Crea y persiste una nueva propiedad."""
        pass

    def update(self, property_id: int, propertyDTO: RealEstateDTO, current_user: UserDTO | None = None) -> RealEstateDTO | None:
        """Actualiza los datos de una propiedad existente."""
        pass

    def delete(self, property_id: int, current_user: UserDTO | None = None) -> bool:
        """Elimina una propiedad por su ID."""
        pass

    def get_favorites(self, user_id: int, skip: int = 0, limit: int = 100) -> list[RealEstateDTO]:
        """Obtiene las propiedades marcadas como favoritas por un usuario."""
        pass

