# models/leads.py
from datetime import datetime
from typing import Optional
# pyrefly: ignore [missing-import]
from sqlalchemy import Integer, DateTime, ForeignKey, Identity, Boolean
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel, ConfigDict, field_validator
from Repositories.database import Base


class LeadDTO(Base):
    """Modelo SQLAlchemy para la tabla lead."""
    __tablename__ = "lead"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.users.id"), nullable=False)
    id_real_state: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("inverclick.real_estate.id"), nullable=True)
    id_constructionCompany: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("inverclick.construction_company.id"), nullable=True)
    is_favorite: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)


# --- Esquemas Pydantic ---

class LeadCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_user: Optional[int] = None
    id_real_state: Optional[int] = None
    id_constructionCompany: Optional[int] = None
    is_favorite: Optional[bool] = True

    @field_validator("id_user", "id_real_state", "id_constructionCompany", mode="before")
    @classmethod
    def convert_zero_to_none(cls, v):
        if v is not None and isinstance(v, (int, float, str)):
            try:
                if int(v) <= 0:
                    return None
            except ValueError:
                pass
        return v


class LeadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, coerce_numbers_to_str=True)

    id: int
    id_user: int
    id_real_state: Optional[int] = None
    id_constructionCompany: Optional[int] = None
    is_favorite: Optional[bool] = True
    created_at: Optional[datetime] = None

