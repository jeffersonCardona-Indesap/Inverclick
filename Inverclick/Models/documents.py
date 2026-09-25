# documents.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class DocumentDTO(Base):
    __tablename__ = "documentos"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    id_user: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("inverclick.users.id", ondelete="CASCADE"), 
        nullable=False
    )
    document_name: Mapped[str] = mapped_column(String(255), nullable=False)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class DocumentCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id_user: int
    document_name: str
    document_type: str
    location: str

class DocumentUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    document_name: Optional[str] = None
    document_type: Optional[str] = None
    location: Optional[str] = None

class DocumentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_user: int
    document_name: str
    document_type: str
    location: str
    created_at: Optional[datetime] = None
