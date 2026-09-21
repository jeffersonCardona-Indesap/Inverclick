# models/constructoras.py
from datetime import datetime
from typing import Optional
# pyrefly: ignore [missing-import]
from sqlalchemy import String, Integer, DateTime, Float, Text, Identity
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class ConstructionCompanyDTO(Base):
    """Modelo SQLAlchemy para la tabla construction_company."""
    __tablename__ = "construction_company"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    nit: Mapped[str] = mapped_column(String(100), nullable=False)
    Nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    Address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    Description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    Rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)


# --- Esquemas Pydantic ---

class ConstructoraCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nit: str
    Nombre: str
    phone_number: Optional[str] = None
    Address: Optional[str] = None
    Description: Optional[str] = None
    Rating: Optional[float] = None
    email: Optional[str] = None


class ConstructoraUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nit: Optional[str] = None
    Nombre: Optional[str] = None
    phone_number: Optional[str] = None
    Address: Optional[str] = None
    Description: Optional[str] = None
    Rating: Optional[float] = None
    email: Optional[str] = None


class ConstructoraResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, coerce_numbers_to_str=True)


    id: int
    nit: str
    Nombre: str
    phone_number: Optional[str] = None
    Address: Optional[str] = None
    Description: Optional[str] = None
    created_at: Optional[datetime] = None
    Rating: Optional[float] = None
    email: Optional[str] = None
