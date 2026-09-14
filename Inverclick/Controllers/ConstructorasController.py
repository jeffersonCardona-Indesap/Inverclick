# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Services.IConstructorasService import IConstructorasService
from Services.Impl.ConstructorasService import ConstructorasService
from Repositories.ConstructorasRepository import ConstructorasRepository
from Utils.HttpResponses.constructoraHttpResponses import ConstructoraHttpResponses
from Repositories.database import get_db
from Models.constructoras import (
    ConstructionCompanyDTO,
    ConstructoraCreateSchema,
    ConstructoraUpdateSchema,
    ConstructoraResponseSchema,
)
from Models.users import UserDTO
from Utils.auth_middleware import RoleChecker, get_current_user

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/constructoras", tags=["Constructoras"])

role_master_or_admin = RoleChecker(["Master", "Admin"])
role_constructora = RoleChecker(["Master", "Admin", "Constructora"])


def get_constructoras_service(db: Session = Depends(get_db)) -> IConstructorasService:
    repository = ConstructorasRepository(db)
    http_responses = ConstructoraHttpResponses()
    return ConstructorasService(repository, http_responses)


# --- Endpoints del API ---

@router.get("", response_model=list[ConstructoraResponseSchema])
def get_all_constructoras(
    skip: int = 0,
    limit: int = 100,
    service: IConstructorasService = Depends(get_constructoras_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Obtiene todas las constructoras (solo Master y Admin)."""
    return service.get_all(skip=skip, limit=limit)


@router.get("/{company_id}", response_model=ConstructoraResponseSchema)
def get_constructora_by_id(
    company_id: int,
    service: IConstructorasService = Depends(get_constructoras_service),
    current_user: UserDTO = Depends(role_constructora),
):
    """Obtiene una constructora por su ID."""
    return service.get_by_id(company_id)


@router.post("", status_code=201, response_model=ConstructoraResponseSchema)
def create_constructora(
    company: ConstructoraCreateSchema,
    service: IConstructorasService = Depends(get_constructoras_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Crea una nueva constructora (solo Master y Admin)."""
    company_dto = ConstructionCompanyDTO(**company.model_dump(exclude_none=True))
    return service.create(company_dto)


@router.put("/{company_id}", response_model=ConstructoraResponseSchema)
def update_constructora(
    company_id: int,
    company: ConstructoraUpdateSchema,
    service: IConstructorasService = Depends(get_constructoras_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Actualiza una constructora existente (solo Master y Admin)."""
    company_dto = ConstructionCompanyDTO(**company.model_dump(exclude_unset=True))
    return service.update(company_id=company_id, companyDTO=company_dto)


@router.delete("/{company_id}")
def delete_constructora(
    company_id: int,
    service: IConstructorasService = Depends(get_constructoras_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Elimina una constructora (solo Master y Admin)."""
    return {"success": service.delete(company_id)}
