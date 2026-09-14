# models/leads.py
from datetime import datetime
from typing import Optional
# pyrefly: ignore [missing-import]
from sqlalchemy import Integer, DateTime, ForeignKey, Identity
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class LeadDTO(Base):
    """Modelo SQLAlchemy para la tabla lead."""
    __tablename__ = "lead"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.users.id"), nullable=False)
    id_real_state: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.real_estate.id"), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)


# --- Esquemas Pydantic ---

class LeadCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_user: int
    id_real_state: int


class LeadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_user: int
    id_real_state: int
    created_at: Optional[datetime] = None
