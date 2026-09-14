from Models.sales import SaleDTO


class ISalesService:
    """
    Interfaz para el servicio de ventas.
    """
    def get_by_id(self, sale_id: int) -> SaleDTO | None:
        """Obtiene una venta por su ID."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        """Obtiene una lista paginada de todas las ventas."""
        pass

    def create(self, saleDTO: SaleDTO) -> SaleDTO:
        """Registra una nueva venta, aplicando todas las reglas de negocio."""
        pass
