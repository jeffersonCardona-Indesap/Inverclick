# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Services.ILeadsService import ILeadsService
from Services.Impl.LeadsService import LeadsService
from Repositories.LeadsRepository import LeadsRepository
from Repositories.UsersRepository import UsersRepository
from Repositories.PropertiesRepository import PropertiesRepository
from Utils.HttpResponses.leadHttpResponses import LeadHttpResponses
from Repositories.database import get_db
from Models.leads import LeadDTO, LeadCreateSchema, LeadResponseSchema
from Models.users import UserDTO
from Utils.auth_middleware import RoleChecker

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/leads", tags=["Leads"])

role_master_or_admin = RoleChecker(["Master", "Admin"])
role_all_authorized = RoleChecker(["Master", "Admin", "Constructora"])


def get_leads_service(db: Session = Depends(get_db)) -> ILeadsService:
    repository = LeadsRepository(db)
    users_repository = UsersRepository(db)
    properties_repository = PropertiesRepository(db)
    http_responses = LeadHttpResponses()
    return LeadsService(repository, users_repository, properties_repository, http_responses)


# --- Endpoints del API ---

@router.get("", response_model=list[LeadResponseSchema])
def get_all_leads(
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene todos los leads."""
    return service.get_all(skip=skip, limit=limit)


@router.get("/{lead_id}", response_model=LeadResponseSchema)
def get_lead_by_id(
    lead_id: int,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene un lead por su ID."""
    return service.get_by_id(lead_id)


@router.get("/user/{user_id}", response_model=list[LeadResponseSchema])
def get_leads_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene los leads de un usuario específico."""
    return service.get_by_user(user_id, skip=skip, limit=limit)


@router.get("/property/{real_estate_id}", response_model=list[LeadResponseSchema])
def get_leads_by_property(
    real_estate_id: int,
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene los leads asociados a una propiedad."""
    return service.get_by_property(real_estate_id, skip=skip, limit=limit)


@router.post("", status_code=201, response_model=LeadResponseSchema)
def create_lead(
    lead: LeadCreateSchema,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Crea un nuevo lead."""
    lead_dto = LeadDTO(**lead.model_dump(exclude_none=True))
    return service.create(lead_dto)


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Elimina un lead."""
    return {"success": service.delete(lead_id)}
