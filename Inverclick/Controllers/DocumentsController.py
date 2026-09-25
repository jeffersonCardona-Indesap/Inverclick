# DocumentsController.py
from typing import Optional, Any
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.DocumentsRepository import DocumentsRepository
from Repositories.UsuariosRepository import UsersRepository
from Utils.HttpResponses.documentsHttpResponses import DocumentsHttpResponses
from Services.IDocumentsService import IDocumentsService
from Services.Impl.DocumentsService import DocumentsService
from Services.Security.AuthDependencies import get_current_user

# Configuración del enrutador de Documentos
router = APIRouter(prefix="/documents", tags=["Documents"])

def get_documents_service(db: Session = Depends(get_db)) -> IDocumentsService:
    repository = DocumentsRepository(db)
    http_responses = DocumentsHttpResponses()
    users_repository = UsersRepository(db)
    return DocumentsService(repository, http_responses, users_repository)

@router.post("/upload", response_class=JSONResponse, status_code=201)
def upload_document(
    file: UploadFile = File(..., description="Archivo a subir (PDF, PNG, JPG, CSV, XLSX según rol)"),
    user_id_target: Optional[int] = Form(None, description="ID del usuario asociado (opcional, por defecto el usuario autenticado)"),
    link_to_profile: bool = Form(False, description="Vincular este documento como id_document del usuario"),
    current_user: dict[str, Any] = Depends(get_current_user),
    service: IDocumentsService = Depends(get_documents_service)
):
    """
    Carga un archivo y almacena sus metadatos con validación estricta de extensiones según el rol:
    - Administrador / Constructora / Ventas: PDF, PNG, JPG, CSV, XLSX
    - Cliente: estrictamente PDF
    """
    saved_doc = service.upload_document(
        file=file,
        current_user=current_user,
        user_id_target=user_id_target,
        link_to_profile=link_to_profile
    )
    return DocumentsHttpResponses.success_uploaded(saved_doc)

@router.get("/{document_id}", response_class=JSONResponse)
def get_document_by_id(
    document_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: IDocumentsService = Depends(get_documents_service)
):
    """Obtiene los metadatos de un documento por su ID."""
    doc = service.get_by_id(document_id, current_user)
    return DocumentsHttpResponses.success_get(doc)

@router.get("/user/{user_id}", response_class=JSONResponse)
def get_documents_by_user(
    user_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: IDocumentsService = Depends(get_documents_service)
):
    """Obtiene todos los documentos asociados a un usuario."""
    docs = service.get_by_user_id(user_id, current_user)
    return DocumentsHttpResponses.success_get_all(docs)

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: IDocumentsService = Depends(get_documents_service)
):
    """Descarga el archivo físico del almacenamiento externo."""
    file_path, filename, media_type = service.get_file_path(document_id, current_user)
    return FileResponse(path=file_path, filename=filename, media_type=media_type)

@router.delete("/{document_id}", response_class=JSONResponse)
def delete_document(
    document_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: IDocumentsService = Depends(get_documents_service)
):
    """Elimina un documento de la base de datos y del almacenamiento físico."""
    service.delete_document(document_id, current_user)
    return DocumentsHttpResponses.success_deleted()
