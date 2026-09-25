# construction_company.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, Text, Float, DateTime, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class ConstructionCompanyDTO(Base):
    __tablename__ = "construction_company"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=False, start=1), primary_key=True)
    nit: Mapped[str] = mapped_column(Text, nullable=False)
    Nombre: Mapped[str] = mapped_column("Nombre", String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    Address: Mapped[str] = mapped_column("Address", Text, nullable=False)
    Description: Mapped[str] = mapped_column("Description", Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    Rating: Mapped[Optional[float]] = mapped_column("Rating", Float, nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class ConstructionCompanyCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nit: str
    Nombre: str
    phone_number: str
    Address: str
    Description: str
    Rating: Optional[float] = None
    email: str

class ConstructionCompanyUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nit: Optional[str] = None
    Nombre: Optional[str] = None
    phone_number: Optional[str] = None
    Address: Optional[str] = None
    Description: Optional[str] = None
    Rating: Optional[float] = None
    email: Optional[str] = None

class ConstructionCompanyResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nit: str
    Nombre: str
    phone_number: str
    Address: str
    Description: str
    created_at: Optional[datetime] = None
    Rating: Optional[float] = None
    email: str
