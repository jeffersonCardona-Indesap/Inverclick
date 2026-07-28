from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Prefix(Base):
    __tablename__ = "prefix"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
