# DocumentsRepository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.documents import DocumentDTO
from Repositories.IDocumentsRepository import IDocumentsRepository

class DocumentsRepository(IDocumentsRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        """Obtiene un documento por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(DocumentDTO).where(DocumentDTO.id == document_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: int) -> list[DocumentDTO]:
        """Obtiene todos los documentos asociados a un ID de usuario."""
        statement = select(DocumentDTO).where(DocumentDTO.id_user == user_id)
        return list(self.db.execute(statement).scalars().all())

    def create(self, document_dto: DocumentDTO) -> DocumentDTO:
        """Crea y persiste un nuevo documento en la base de datos."""
        self.db.add(document_dto)
        self.db.commit()
        self.db.refresh(document_dto)
        return document_dto

    def delete(self, document_id: int) -> bool:
        """Elimina un documento por su ID."""
        documento = self.get_by_id(document_id)
        if documento:
            self.db.delete(documento)
            self.db.commit()
            return True
        return False
