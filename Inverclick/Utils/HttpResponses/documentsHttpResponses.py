# documentsHttpResponses.py
from typing import Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.documents import DocumentDTO, DocumentResponseSchema

class DocumentsHttpResponses:
    @staticmethod
    def success_uploaded(document_dto: DocumentDTO | DocumentResponseSchema | dict[str, Any]) -> JSONResponse:
        data = document_dto if isinstance(document_dto, dict) else (
            DocumentResponseSchema.model_validate(document_dto).model_dump(mode="json")
        )
        return success_response(data, "Documento subido y registrado exitosamente", 201)

    @staticmethod
    def success_get(document_dto: DocumentDTO | DocumentResponseSchema | dict[str, Any]) -> JSONResponse:
        data = document_dto if isinstance(document_dto, dict) else (
            DocumentResponseSchema.model_validate(document_dto).model_dump(mode="json")
        )
        return success_response(data, "Documento obtenido exitosamente", 200)

    @staticmethod
    def success_get_all(documents: list[Any]) -> JSONResponse:
        data = [
            doc if isinstance(doc, dict) else DocumentResponseSchema.model_validate(doc).model_dump(mode="json")
            for doc in documents
        ]
        return success_response(data, "Documentos obtenidos exitosamente", 200)

    @staticmethod
    def success_deleted() -> JSONResponse:
        return success_response(None, "Documento eliminado exitosamente", 200)

    @staticmethod
    def error_invalid_format(role: str, filename: str) -> HTTPException:
        return HTTPException(
            status_code=400,
            detail=f"Formato o extensión no permitida para el rol '{role}'. Archivo recibido: '{filename}'."
        )

    @staticmethod
    def error_client_pdf_only() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="Los usuarios con rol Cliente solo tienen permitido subir y gestionar archivos en formato PDF."
        )

    @staticmethod
    def error_document_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Documento no encontrado")

    @staticmethod
    def error_user_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Usuario no encontrado en el sistema")

    @staticmethod
    def error_file_empty() -> HTTPException:
        return HTTPException(status_code=400, detail="El archivo enviado está vacío o no contiene datos válidos")

    @staticmethod
    def error_storage_failed(detail: str) -> HTTPException:
        return HTTPException(
            status_code=500,
            detail=f"Error interno al almacenar el archivo en la ubicación externa: {detail}"
        )
