# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Models.sales import SaleDTO
from Repositories.ISalesRepository import ISalesRepository


class SalesRepository(ISalesRepository):
    """Implementación SQLAlchemy para el repositorio de ventas."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sale_id: int) -> SaleDTO | None:
        """Obtiene una venta por su ID."""
        statement = select(SaleDTO).where(SaleDTO.id == sale_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_real_estate_id(self, real_estate_id: int) -> SaleDTO | None:
        """Obtiene la venta asociada a una propiedad específica."""
        statement = select(SaleDTO).where(SaleDTO.real_estate_id == real_estate_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        """Obtiene una lista paginada de todas las ventas."""
        statement = select(SaleDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, saleDTO: SaleDTO) -> SaleDTO:
        """Crea y persiste una nueva venta en la base de datos."""
        self.db.add(saleDTO)
        self.db.commit()
        self.db.refresh(saleDTO)
        return saleDTO
