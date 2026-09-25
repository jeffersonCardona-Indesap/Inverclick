# lead.py
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Integer, Boolean, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class LeadDTO(Base):
    __tablename__ = "lead"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=False, start=1), primary_key=True)
    id_user: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("inverclick.users.id"), nullable=True)
    id_real_state: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("inverclick.real_estate.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    id_constructionCompany: Mapped[Optional[int]] = mapped_column("id_constructionCompany", Integer, ForeignKey("inverclick.construction_company.id"), nullable=True)
    is_favorite: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, nullable=True)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class LeadCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_user: Optional[int] = None
    id_real_state: Optional[int] = None
    id_constructionCompany: Optional[int] = None
    is_favorite: Optional[bool] = True

class LeadUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_user: Optional[int] = None
    id_real_state: Optional[int] = None
    id_constructionCompany: Optional[int] = None
    is_favorite: Optional[bool] = None

class LeadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_user: Optional[int] = None
    id_real_state: Optional[int] = None
    created_at: Optional[datetime] = None
    id_constructionCompany: Optional[int] = None
    is_favorite: Optional[bool] = True
