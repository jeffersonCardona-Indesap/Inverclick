# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Services.ILeadsService import ILeadsService
from Services.Impl.LeadsService import LeadsService
from Repositories.LeadsRepository import LeadsRepository
from Repositories.UsersRepository import UsersRepository
from Repositories.PropertiesRepository import PropertiesRepository
from Repositories.ConstructorasRepository import ConstructorasRepository
from Utils.HttpResponses.leadHttpResponses import LeadHttpResponses
from Repositories.database import get_db
from Models.leads import LeadDTO, LeadCreateSchema, LeadResponseSchema
from Models.users import UserDTO
from Utils.auth_middleware import RoleChecker


# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/leads", tags=["Leads"])

role_master_or_admin = RoleChecker(["Master", "Admin"])
role_all_authorized = RoleChecker(["Master", "Admin", "Constructora", "Usuario"])


def get_leads_service(db: Session = Depends(get_db)) -> ILeadsService:
    repository = LeadsRepository(db)
    users_repository = UsersRepository(db)
    properties_repository = PropertiesRepository(db)
    constructoras_repository = ConstructorasRepository(db)
    http_responses = LeadHttpResponses()
    return LeadsService(repository, users_repository, properties_repository, http_responses, constructoras_repository)


# --- Endpoints del API ---

@router.get("", response_model=list[LeadResponseSchema])
def get_all_leads(
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene los leads (filtrados según el rol del usuario autenticado)."""
    return service.get_all(skip=skip, limit=limit, current_user=current_user)


@router.get("/favorites", response_model=list[LeadResponseSchema])
def get_user_favorite_leads(
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene todos los leads activos marcados como favoritos por el usuario autenticado."""
    return service.get_favorites(current_user=current_user, skip=skip, limit=limit)


@router.get("/{lead_id}", response_model=LeadResponseSchema)
def get_lead_by_id(
    lead_id: int,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene un lead por su ID."""
    return service.get_by_id(lead_id, current_user=current_user)


@router.get("/user/{user_id}", response_model=list[LeadResponseSchema])
def get_leads_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene los leads de un usuario específico."""
    return service.get_by_user(user_id, skip=skip, limit=limit, current_user=current_user)


@router.get("/property/{real_estate_id}", response_model=list[LeadResponseSchema])
def get_leads_by_property(
    real_estate_id: int,
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene los leads asociados a una propiedad."""
    return service.get_by_property(real_estate_id, skip=skip, limit=limit, current_user=current_user)


@router.post("", status_code=201, response_model=LeadResponseSchema)
def create_lead_or_favorite(
    lead: LeadCreateSchema,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Registra o conmuta un favorito / lead (Master, Admin, Constructora, Usuario)."""
    lead_dto = LeadDTO(**lead.model_dump(exclude_none=True))
    return service.create(lead_dto, current_user=current_user)


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    service: ILeadsService = Depends(get_leads_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Elimina un lead."""
    return {"success": service.delete(lead_id, current_user=current_user)}

