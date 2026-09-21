from Models.leads import LeadDTO


class ILeadsRepository:
    """
    Interfaz para el repositorio de leads.
    """
    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        """Obtiene un lead por su ID."""
        pass

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads de un usuario específico."""
        pass

    def get_favorites_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads activos marcados como favoritos por un usuario específico."""
        pass

    def get_by_real_estate_id(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads asociados a una propiedad específica."""
        pass

    def get_by_constructora_id(self, constructora_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene los leads asociados a una constructora específica."""
        pass

    def get_by_user_and_target(self, user_id: int, real_estate_id: int | None = None, constructora_id: int | None = None) -> LeadDTO | None:
        """Busca un lead existente por usuario y propiedad o constructora objetivo."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        """Obtiene una lista paginada de todos los leads."""
        pass

    def create(self, leadDTO: LeadDTO) -> LeadDTO:
        """Crea y persiste un nuevo lead en la base de datos."""
        pass

    def update(self, lead_id: int, data: dict) -> LeadDTO | None:
        """Actualiza los datos de un lead."""
        pass

    def delete(self, lead_id: int) -> bool:
        """Elimina un lead por su ID."""
        pass

