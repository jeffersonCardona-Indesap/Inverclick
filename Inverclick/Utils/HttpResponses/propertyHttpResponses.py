from fastapi import HTTPException


class PropertyHttpResponses:
    """Respuestas HTTP estandarizadas para el módulo de propiedades."""

    @staticmethod
    def error_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Propiedad no encontrada")

    @staticmethod
    def error_name_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Ya existe una propiedad con ese nombre")

    @staticmethod
    def error_address_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Ya existe una propiedad con esa dirección")

    @staticmethod
    def error_constructora_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="La constructora asociada no existe")

    @staticmethod
    def error_missing_price() -> HTTPException:
        return HTTPException(status_code=400, detail="El precio es un campo obligatorio")

    @staticmethod
    def error_missing_constructora() -> HTTPException:
        return HTTPException(status_code=400, detail="La constructora asociada (id_constructionCompany) es un campo obligatorio")

    @staticmethod
    def error_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo crear la propiedad")

    @staticmethod
    def error_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo actualizar la propiedad")

    @staticmethod
    def error_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo eliminar la propiedad")

    @staticmethod
    def error_already_sold() -> HTTPException:
        return HTTPException(status_code=409, detail="Esta propiedad ya fue vendida y no puede modificarse")
