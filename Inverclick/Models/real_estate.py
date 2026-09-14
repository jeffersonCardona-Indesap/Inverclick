# models/real_estate.py
from datetime import datetime
from typing import Optional
# pyrefly: ignore [missing-import]
from sqlalchemy import String, Integer, DateTime, Float, Text, Boolean, ForeignKey, Identity
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class RealEstateDTO(Base):
    """Modelo SQLAlchemy para la tabla real_estate."""
    __tablename__ = "real_estate"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    id_constructionCompany: Mapped[int] = mapped_column(
        Integer, ForeignKey("inverclick.construction_company.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    stock: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)
    sales_status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)


# --- Esquemas Pydantic ---

class RealEstateCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_constructionCompany: int
    name: str
    stock: Optional[int] = None
    price: float
    city: Optional[str] = None
    zip_code: Optional[str] = None
    address: str
    description: Optional[str] = None
    status: Optional[bool] = True
    sales_status: Optional[bool] = False


class RealEstateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_constructionCompany: Optional[int] = None
    name: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    sales_status: Optional[bool] = None


class RealEstateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_constructionCompany: int
    name: str
    stock: Optional[int] = None
    created_at: Optional[datetime] = None
    price: float
    city: Optional[str] = None
    zip_code: Optional[str] = None
    address: str
    description: Optional[str] = None
    status: Optional[bool] = None
    sales_status: Optional[bool] = None
