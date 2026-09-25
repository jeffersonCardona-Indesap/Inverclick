# real_estate.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, Text, Float, Boolean, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class RealEstateDTO(Base):
    __tablename__ = "real_estate"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=False, start=1), primary_key=True)
    id_constructionCompany: Mapped[int] = mapped_column(
        "id_constructionCompany", 
        BigInteger, 
        ForeignKey("inverclick.construction_company.id"), 
        nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stock: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    zip_code: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)
    sales_status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class RealEstateCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_constructionCompany: int
    name: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    city: Optional[str] = None
    zip_code: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = True
    sales_status: Optional[bool] = True

class RealEstateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_constructionCompany: Optional[int] = None
    name: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    city: Optional[str] = None
    zip_code: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    sales_status: Optional[bool] = None

class RealEstateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_constructionCompany: int
    name: Optional[str] = None
    stock: Optional[int] = None
    created_at: Optional[datetime] = None
    price: Optional[float] = None
    city: Optional[str] = None
    zip_code: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = True
    sales_status: Optional[bool] = True
