from Models.audit_log import AuditLogDTO


class IAuditLogRepository:
    """
    Interfaz para el repositorio de logs de auditoría.
    """
    def create(self, logDTO: AuditLogDTO) -> AuditLogDTO:
        """Registra un nuevo log de auditoría en la base de datos."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditLogDTO]:
        """Obtiene una lista paginada de los logs de auditoría."""
        pass

    def get_by_entity(self, entity_type: str, entity_id: int) -> list[AuditLogDTO]:
        """Obtiene los logs de auditoría para una entidad específica."""
        pass

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[AuditLogDTO]:
        """Obtiene los logs de auditoría de un usuario específico."""
        pass
