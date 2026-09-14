# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Models.audit_log import AuditLogDTO
from Repositories.IAuditLogRepository import IAuditLogRepository


class AuditLogRepository(IAuditLogRepository):
    """Implementación SQLAlchemy para el repositorio de logs de auditoría."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, logDTO: AuditLogDTO) -> AuditLogDTO:
        """Registra un nuevo log de auditoría en la base de datos."""
        self.db.add(logDTO)
        self.db.commit()
        self.db.refresh(logDTO)
        return logDTO

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditLogDTO]:
        """Obtiene una lista paginada de los logs de auditoría."""
        statement = select(AuditLogDTO).order_by(AuditLogDTO.created_at.desc()).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def get_by_entity(self, entity_type: str, entity_id: int) -> list[AuditLogDTO]:
        """Obtiene los logs de auditoría para una entidad específica."""
        statement = (
            select(AuditLogDTO)
            .where(AuditLogDTO.entity_type == entity_type, AuditLogDTO.entity_id == entity_id)
            .order_by(AuditLogDTO.created_at.desc())
        )
        return list(self.db.execute(statement).scalars().all())

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[AuditLogDTO]:
        """Obtiene los logs de auditoría de un usuario específico."""
        statement = (
            select(AuditLogDTO)
            .where(AuditLogDTO.user_id == user_id)
            .order_by(AuditLogDTO.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())
