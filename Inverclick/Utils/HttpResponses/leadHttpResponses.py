
# pyrefly: ignore [missing-import]
from fastapi import HTTPException


class LeadHttpResponses:
    """Respuestas HTTP estandarizadas para el módulo de leads."""

    @staticmethod
    def error_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Lead no encontrado")

    @staticmethod
    def error_user_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="El usuario asociado al lead no existe")

    @staticmethod
    def error_property_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="La propiedad asociada al lead no existe")

    @staticmethod
    def error_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo crear el lead")

    @staticmethod
    def error_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo eliminar el lead")
