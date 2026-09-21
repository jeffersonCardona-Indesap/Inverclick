from Models.leads import LeadDTO
from Models.users import UserDTO


class ILeadsService:
    """
    Interfaz para el servicio de leads.
    """
    def get_by_id(self, lead_id: int, current_user: UserDTO | None = None) -> LeadDTO | None:
        """Obtiene un lead por su ID."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[LeadDTO]:
        """Obtiene una lista paginada de leads filtrada según el rol del usuario."""
        pass

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[LeadDTO]:
        """Obtiene los leads de un usuario específico."""
        pass

    def get_by_property(self, real_estate_id: int, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[LeadDTO]:
        """Obtiene los leads de una propiedad específica."""
        pass

    def create(self, leadDTO: LeadDTO, current_user: UserDTO | None = None) -> LeadDTO:
        """Crea y persiste un nuevo lead o marca/desmarca favorito."""
        pass

    def toggle_favorite(self, leadDTO: LeadDTO, current_user: UserDTO) -> LeadDTO:
        """Marca o desmarca una propiedad o constructora como favorita registrando el lead."""
        pass

    def delete(self, lead_id: int, current_user: UserDTO | None = None) -> bool:
        """Elimina un lead por su ID."""
        pass

    def get_favorites(self, current_user: UserDTO, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads activos marcados como favoritos por el usuario actual."""
        pass

