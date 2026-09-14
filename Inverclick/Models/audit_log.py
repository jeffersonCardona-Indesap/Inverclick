# models/audit_log.py
from datetime import datetime
from typing import Optional
# pyrefly: ignore [missing-import]
from sqlalchemy import String, Integer, DateTime, Text, Identity
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base


class AuditLogDTO(Base):
    """
    Modelo SQLAlchemy para la tabla audit_logs.
    Registra las acciones críticas del sistema con trazabilidad completa.
    """
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, SALE
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)  # constructora, property, lead, sale
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    endpoint: Mapped[str] = mapped_column(String(300), nullable=False)
    method: Mapped[str] = mapped_column(String(10), nullable=False)  # POST, PUT, DELETE
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
