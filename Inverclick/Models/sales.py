# models/sales.py
from datetime import datetime
from typing import Optional
# pyrefly: ignore [missing-import]
from sqlalchemy import Integer, DateTime, Float, Text, ForeignKey, Identity
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class SaleDTO(Base):
    """
    Modelo SQLAlchemy para la tabla sales.
    Registra la trazabilidad completa de una venta:
    lead que generó la conversión, vendedor, comprador y propiedad.
    """
    __tablename__ = "sales"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.lead.id"), nullable=False)
    seller_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.users.id"), nullable=False)
    buyer_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.users.id"), nullable=False)
    real_estate_id: Mapped[int] = mapped_column(Integer, ForeignKey("inverclick.real_estate.id"), nullable=False)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sale_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)


# --- Esquemas Pydantic ---

class SaleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    lead_id: int
    seller_user_id: int
    buyer_user_id: int
    real_estate_id: int
    sale_price: float
    notes: Optional[str] = None


class SaleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    seller_user_id: int
    buyer_user_id: int
    real_estate_id: int
    sale_price: float
    notes: Optional[str] = None
    sale_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
