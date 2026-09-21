# pyrefly: ignore [missing-import]
from fastapi import HTTPException


class ConstructoraHttpResponses:
    """Respuestas HTTP estandarizadas para el módulo de constructoras."""

    @staticmethod
    def error_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Constructora no encontrada")

    @staticmethod
    def error_nit_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Ya existe una constructora con ese NIT")

    @staticmethod
    def error_nombre_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Ya existe una constructora con ese nombre")

    @staticmethod
    def error_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo crear la constructora")

    @staticmethod
    def error_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo actualizar la constructora")

    @staticmethod
    def error_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="No se pudo eliminar la constructora")
