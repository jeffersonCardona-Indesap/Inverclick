# DocumentsService.py
import os
import shutil
import re
from pathlib import Path
from uuid import uuid4
from typing import Any, Optional
from fastapi import UploadFile, HTTPException
from Models.documents import DocumentDTO
from Repositories.IDocumentsRepository import IDocumentsRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Utils.HttpResponses.documentsHttpResponses import DocumentsHttpResponses
from Services.IDocumentsService import IDocumentsService

# Extensiones permitidas según especificación de negocio (CA1)
CORPORATE_ROLES = {"master", "admin", "administrador", "constructora", "ventas"}
CORPORATE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".csv", ".xlsx"}
CLIENT_EXTENSIONS = {".pdf"}

class DocumentsService(IDocumentsService):
    def __init__(
        self,
        repository: IDocumentsRepository,
        http_responses: DocumentsHttpResponses,
        users_repository: Optional[IUsuariosRepository] = None,
        storage_path: Optional[str] = None
    ):
        self.repository = repository
        self.http_responses = http_responses
        self.users_repository = users_repository
        
        # Resolución de la ruta de almacenamiento externo (CA2)
        project_root = Path(__file__).resolve().parents[2]
        configured_path = storage_path or os.getenv("EXTERNAL_STORAGE_PATH")

        if configured_path:
            resolved = Path(configured_path).resolve()
        else:
            # Por defecto, almacenar en un directorio hermano fuera de la raíz del código backend
            resolved = (project_root.parent / "inverclick_external_storage").resolve()

        # Validación estricta de aislamiento: nunca almacenar dentro del código fuente del backend
        try:
            if resolved == project_root or project_root in resolved.parents:
                resolved = (project_root.parent / "inverclick_external_storage").resolve()
        except Exception:
            pass

        self.storage_directory = str(resolved)
        os.makedirs(self.storage_directory, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza el nombre de archivo preservando su extensión."""
        clean = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
        return clean.strip('_') or "document"

    def _validate_role_format(self, role: str, filename: str) -> str:
        """Valida que la extensión del archivo cumpla con los formatos permitidos para el rol (CA1)."""
        ext = Path(filename).suffix.lower()
        if not ext:
            raise HTTPException(status_code=400, detail="El archivo no contiene una extensión válida.")

        role_lower = role.strip().lower()

        if role_lower == "cliente":
            if ext not in CLIENT_EXTENSIONS:
                raise self.http_responses.error_client_pdf_only()
            return ext

        if role_lower in CORPORATE_ROLES:
            if ext not in CORPORATE_EXTENSIONS:
                raise self.http_responses.error_invalid_format(role, filename)
            return ext

        # Otros roles: por defecto se limita a PDF por seguridad
        if ext not in CLIENT_EXTENSIONS:
            raise self.http_responses.error_invalid_format(role, filename)
        return ext

    def upload_document(
        self,
        file: UploadFile,
        current_user: dict[str, Any],
        user_id_target: Optional[int] = None,
        link_to_profile: bool = False
    ) -> DocumentDTO:
        if not file or not file.filename:
            raise self.http_responses.error_file_empty()

        user_role = str(current_user.get("role", "Cliente")).strip()
        auth_user_id = current_user.get("user_id")

        # 1. Validar extensión según rol del usuario (CA1)
        ext = self._validate_role_format(user_role, file.filename)

        # 2. Determinar el usuario dueño del documento
        target_id = user_id_target if user_id_target is not None else auth_user_id
        if not target_id:
            raise self.http_responses.error_user_not_found()

        # Si un cliente intenta subir un documento para otro usuario, rechazar
        if user_role.lower() == "cliente" and target_id != auth_user_id:
            raise HTTPException(
                status_code=403,
                detail="Un usuario con rol Cliente no puede asociar documentos a otros usuarios."
            )

        # Verificar existencia del usuario si el repositorio está disponible
        if self.users_repository:
            user = self.users_repository.get_by_id(target_id)
            if not user:
                raise self.http_responses.error_user_not_found()

        # 3. Guardar físicamente el archivo en el directorio externo aislado (CA2)
        safe_name = self._sanitize_filename(file.filename)
        unique_name = f"{uuid4().hex}_{safe_name}"
        destination_path = os.path.join(self.storage_directory, unique_name)

        try:
            with open(destination_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise self.http_responses.error_storage_failed(str(e))

        # 4. Registrar metadatos en la base de datos (CA3)
        doc_type = file.content_type or f"application/{ext.replace('.', '')}"
        document_dto = DocumentDTO(
            id_user=target_id,
            document_name=file.filename,
            document_type=doc_type,
            location=destination_path
        )

        saved_document = self.repository.create(document_dto)

        # 5. Si se solicitó vinculación con el perfil de usuario (CA4)
        if link_to_profile and self.users_repository:
            self.users_repository.update(target_id, {"id_document": saved_document.id})

        return saved_document

    def get_by_id(self, document_id: int, current_user: dict[str, Any]) -> DocumentDTO:
        documento = self.repository.get_by_id(document_id)
        if not documento:
            raise self.http_responses.error_document_not_found()

        user_role = str(current_user.get("role", "")).strip().lower()
        auth_user_id = current_user.get("user_id")

        if user_role == "cliente" and documento.id_user != auth_user_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver este documento.")

        return documento

    def get_by_user_id(self, user_id: int, current_user: dict[str, Any]) -> list[DocumentDTO]:
        user_role = str(current_user.get("role", "")).strip().lower()
        auth_user_id = current_user.get("user_id")

        if user_role == "cliente" and user_id != auth_user_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver documentos de otro usuario.")

        return self.repository.get_by_user_id(user_id)

    def get_file_path(self, document_id: int, current_user: dict[str, Any]) -> tuple[str, str, str]:
        documento = self.get_by_id(document_id, current_user)
        
        file_path = documento.location
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="El archivo físico no fue encontrado en el almacenamiento.")

        return file_path, documento.document_name, documento.document_type

    def delete_document(self, document_id: int, current_user: dict[str, Any]) -> bool:
        documento = self.get_by_id(document_id, current_user)

        # Eliminar archivo físico si existe
        if os.path.exists(documento.location):
            try:
                os.remove(documento.location)
            except Exception:
                pass

        return self.repository.delete(document_id)
