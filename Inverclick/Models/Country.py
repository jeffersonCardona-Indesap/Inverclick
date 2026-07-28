from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    iso: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    prefix_id: Mapped[int] = mapped_column(ForeignKey("prefix.id")) 