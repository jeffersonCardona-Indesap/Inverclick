# models.py
from sqlalchemy import Numeric, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Users(Base):
    __tablename__ = "users"

    # Tipado estricto con Mapped y mapped_column
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    zip_code: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    residence_city: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    cell_number: Mapped[float] = mapped_column(Numeric)
    taxes: Mapped[float] = mapped_column(Numeric)
    income: Mapped[float] = mapped_column(Numeric)
    job: Mapped[str] = mapped_column(String(100))
    outcome: Mapped[float] = mapped_column(Numeric)
    id_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Text] = mapped_column(Text)
