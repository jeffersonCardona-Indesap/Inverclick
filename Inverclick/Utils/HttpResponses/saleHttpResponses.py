from fastapi import HTTPException


class SaleHttpResponses:
    """Respuestas HTTP estandarizadas para el módulo de ventas."""

    @staticmethod
    def error_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Venta no encontrada")

    @staticmethod
    def error_lead_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="El lead asociado a la venta no existe")

    @staticmethod
    def error_seller_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="El vendedor (agente de ventas) no existe")

    @staticmethod
    def error_buyer_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="El comprador (cliente final) no existe")

    @staticmethod
    def error_property_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="La propiedad a vender no existe")

    @staticmethod
    def error_property_already_sold() -> HTTPException:
        return HTTPException(
            status_code=409,
            detail="La propiedad ya fue vendida. No se permite la venta múltiple del mismo lote."
        )

    @staticmethod
    def error_property_not_listed() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="La propiedad no se encuentra listada en el catálogo disponible. No se puede ejecutar la venta."
        )

    @staticmethod
    def error_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo registrar la venta")
