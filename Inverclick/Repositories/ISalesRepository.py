from Models.sales import SaleDTO


class ISalesRepository:
    """
    Interfaz para el repositorio de ventas (sales).
    """
    def get_by_id(self, sale_id: int) -> SaleDTO | None:
        """Obtiene una venta por su ID."""
        pass

    def get_by_real_estate_id(self, real_estate_id: int) -> SaleDTO | None:
        """Obtiene la venta asociada a una propiedad específica."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        """Obtiene una lista paginada de todas las ventas."""
        pass

    def create(self, saleDTO: SaleDTO) -> SaleDTO:
        """Crea y persiste una nueva venta en la base de datos."""
        pass
