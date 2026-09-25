# IDocumentsRepository.py
from abc import ABC, abstractmethod
from Models.documents import DocumentDTO

class IDocumentsRepository(ABC):
    """
    Interfaz abstracta para el repositorio de documentos.
    """
    @abstractmethod
    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        """Obtiene un documento por su ID."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[DocumentDTO]:
        """Obtiene todos los documentos asociados a un usuario."""
        pass

    @abstractmethod
    def create(self, document_dto: DocumentDTO) -> DocumentDTO:
        """Crea y persiste un nuevo documento en la base de datos."""
        pass

    @abstractmethod
    def delete(self, document_id: int) -> bool:
        """Elimina un documento por su ID."""
        pass
