from Models.leads import LeadDTO


class ILeadsService:
    """
    Interfaz para el servicio de leads.
    """
    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        """Obtiene un lead por su ID."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene una lista paginada de todos los leads."""
        pass

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads de un usuario específico."""
        pass

    def get_by_property(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads de una propiedad específica."""
        pass

    def create(self, leadDTO: LeadDTO) -> LeadDTO:
        """Crea y persiste un nuevo lead."""
        pass

    def delete(self, lead_id: int) -> bool:
        """Elimina un lead por su ID."""
        pass
