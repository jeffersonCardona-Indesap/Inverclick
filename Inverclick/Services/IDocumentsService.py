# IDocumentsService.py
from abc import ABC, abstractmethod
from typing import Any, Optional
from fastapi import UploadFile
from Models.documents import DocumentDTO

class IDocumentsService(ABC):
    """
    Interfaz para el servicio de gestión documental y almacenamiento externo.
    """
    @abstractmethod
    def upload_document(
        self, 
        file: UploadFile, 
        current_user: dict[str, Any], 
        user_id_target: Optional[int] = None,
        link_to_profile: bool = False
    ) -> DocumentDTO:
        """Sube y registra un nuevo documento con validación por rol y almacenamiento externo."""
        pass

    @abstractmethod
    def get_by_id(self, document_id: int, current_user: dict[str, Any]) -> DocumentDTO:
        """Obtiene los metadatos de un documento por su ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int, current_user: dict[str, Any]) -> list[DocumentDTO]:
        """Obtiene la lista de documentos de un usuario según permisos."""
        pass

    @abstractmethod
    def get_file_path(self, document_id: int, current_user: dict[str, Any]) -> tuple[str, str, str]:
        """Obtiene la ruta física, nombre y tipo MIME de un documento para su descarga."""
        pass

    @abstractmethod
    def delete_document(self, document_id: int, current_user: dict[str, Any]) -> bool:
        """Elimina un documento de la base de datos y del almacenamiento externo."""
        pass
