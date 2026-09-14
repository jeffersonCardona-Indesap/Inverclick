# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Services.IPropertiesService import IPropertiesService
from Services.Impl.PropertiesService import PropertiesService
from Repositories.PropertiesRepository import PropertiesRepository
from Repositories.ConstructorasRepository import ConstructorasRepository
from Utils.HttpResponses.propertyHttpResponses import PropertyHttpResponses
from Repositories.database import get_db
from Models.real_estate import (
    RealEstateDTO,
    RealEstateCreateSchema,
    RealEstateUpdateSchema,
    RealEstateResponseSchema,
)
from Models.users import UserDTO
from Utils.auth_middleware import RoleChecker, get_current_user

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/properties", tags=["Properties"])

role_master_or_admin = RoleChecker(["Master", "Admin"])
role_all_authorized = RoleChecker(["Master", "Admin", "Constructora"])


def get_properties_service(db: Session = Depends(get_db)) -> IPropertiesService:
    repository = PropertiesRepository(db)
    constructoras_repository = ConstructorasRepository(db)
    http_responses = PropertyHttpResponses()
    return PropertiesService(repository, constructoras_repository, http_responses)


# --- Endpoints del API ---

@router.get("", response_model=list[RealEstateResponseSchema])
def get_all_properties(
    skip: int = 0,
    limit: int = 100,
    service: IPropertiesService = Depends(get_properties_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Obtiene todas las propiedades (solo Master y Admin)."""
    return service.get_all(skip=skip, limit=limit)


@router.get("/constructora/{constructora_id}", response_model=list[RealEstateResponseSchema])
def get_properties_by_constructora(
    constructora_id: int,
    skip: int = 0,
    limit: int = 100,
    service: IPropertiesService = Depends(get_properties_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene las propiedades de una constructora específica."""
    return service.get_by_constructora(constructora_id, skip=skip, limit=limit)


@router.get("/{property_id}", response_model=RealEstateResponseSchema)
def get_property_by_id(
    property_id: int,
    service: IPropertiesService = Depends(get_properties_service),
    current_user: UserDTO = Depends(role_all_authorized),
):
    """Obtiene una propiedad por su ID."""
    return service.get_by_id(property_id)


@router.post("", status_code=201, response_model=RealEstateResponseSchema)
def create_property(
    prop: RealEstateCreateSchema,
    service: IPropertiesService = Depends(get_properties_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Crea una nueva propiedad (solo Master y Admin)."""
    prop_dto = RealEstateDTO(**prop.model_dump(exclude_none=True))
    return service.create(prop_dto)


@router.put("/{property_id}", response_model=RealEstateResponseSchema)
def update_property(
    property_id: int,
    prop: RealEstateUpdateSchema,
    service: IPropertiesService = Depends(get_properties_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Actualiza una propiedad existente (solo Master y Admin)."""
    prop_dto = RealEstateDTO(**prop.model_dump(exclude_unset=True))
    return service.update(property_id=property_id, propertyDTO=prop_dto)


@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    service: IPropertiesService = Depends(get_properties_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Elimina una propiedad (solo Master y Admin). No se puede eliminar si ya fue vendida."""
    return {"success": service.delete(property_id)}
