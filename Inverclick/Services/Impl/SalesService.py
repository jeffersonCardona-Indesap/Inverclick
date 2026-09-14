from Repositories.ISalesRepository import ISalesRepository
from Repositories.ILeadsRepository import ILeadsRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Repositories.IPropertiesRepository import IPropertiesRepository
from Models.sales import SaleDTO
from Services.ISalesService import ISalesService
from Utils.HttpResponses.saleHttpResponses import SaleHttpResponses


class SalesService(ISalesService):
    """
    Servicio con lógica de negocio pesada para la gestión de ventas.
    Centraliza las reglas de negocio críticas:
    - Trazabilidad: lead, vendedor, comprador y propiedad son obligatorios (CA3)
    - Disponibilidad: bloquear venta si la propiedad ya fue vendida (CA3)
    - Listado Activo: bloquear venta si la propiedad no está listada (CA3)
    - Al registrar venta: marcar la propiedad como vendida (sales_status=True)
    """

    def __init__(
        self,
        repository: ISalesRepository,
        leads_repository: ILeadsRepository,
        users_repository: IUsuariosRepository,
        properties_repository: IPropertiesRepository,
        http_responses: SaleHttpResponses
    ):
        self.repository = repository
        self.leads_repository = leads_repository
        self.users_repository = users_repository
        self.properties_repository = properties_repository
        self.http_responses = http_responses

    def get_by_id(self, sale_id: int) -> SaleDTO | None:
        sale = self.repository.get_by_id(sale_id)
        if sale is None:
            raise self.http_responses.error_not_found()
        return sale

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        return self.repository.get_all(skip, limit)

    def create(self, saleDTO: SaleDTO) -> SaleDTO:
        """
        Registra una nueva venta aplicando todas las reglas de negocio:
        1. Verificar existencia del lead
        2. Verificar existencia del vendedor (agente de ventas)
        3. Verificar existencia del comprador (cliente final)
        4. Verificar existencia de la propiedad
        5. Regla de Disponibilidad: la propiedad NO debe estar ya vendida
        6. Regla de Listado Activo: la propiedad DEBE estar listada en el catálogo
        7. Registrar la venta y marcar la propiedad como vendida
        """
        # 1. Verificar existencia del lead que generó la conversión
        lead = self.leads_repository.get_by_id(saleDTO.lead_id)
        if lead is None:
            raise self.http_responses.error_lead_not_found()

        # 2. Verificar existencia del vendedor (agente de ventas)
        seller = self.users_repository.get_by_id(saleDTO.seller_user_id)
        if seller is None:
            raise self.http_responses.error_seller_not_found()

        # 3. Verificar existencia del comprador (cliente final)
        buyer = self.users_repository.get_by_id(saleDTO.buyer_user_id)
        if buyer is None:
            raise self.http_responses.error_buyer_not_found()

        # 4. Verificar existencia de la propiedad
        property_obj = self.properties_repository.get_by_id(saleDTO.real_estate_id)
        if property_obj is None:
            raise self.http_responses.error_property_not_found()

        # 5. Regla de Disponibilidad: bloquear si la propiedad ya fue vendida
        if property_obj.sales_status:
            raise self.http_responses.error_property_already_sold()

        # 6. Regla de Listado Activo: bloquear si la propiedad no está listada
        if not property_obj.status:
            raise self.http_responses.error_property_not_listed()

        # 7. Registrar la venta
        result = self.repository.create(saleDTO)
        if result is None:
            raise self.http_responses.error_not_created()

        # 8. Marcar la propiedad como vendida (sales_status = True)
        self.properties_repository.update(
            saleDTO.real_estate_id,
            {"sales_status": True}
        )

        return result
