# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from Services.ISalesService import ISalesService
from Services.Impl.SalesService import SalesService
from Repositories.SalesRepository import SalesRepository
from Repositories.LeadsRepository import LeadsRepository
from Repositories.UsersRepository import UsersRepository
from Repositories.PropertiesRepository import PropertiesRepository
from Utils.HttpResponses.saleHttpResponses import SaleHttpResponses
from Repositories.database import get_db
from Models.sales import SaleDTO, SaleCreateSchema, SaleResponseSchema
from Models.users import UserDTO
from Utils.auth_middleware import RoleChecker

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/sales", tags=["Sales"])

role_master_or_admin = RoleChecker(["Master", "Admin"])


def get_sales_service(db: Session = Depends(get_db)) -> ISalesService:
    repository = SalesRepository(db)
    leads_repository = LeadsRepository(db)
    users_repository = UsersRepository(db)
    properties_repository = PropertiesRepository(db)
    http_responses = SaleHttpResponses()
    return SalesService(repository, leads_repository, users_repository, properties_repository, http_responses)


# --- Endpoints del API ---

@router.get("", response_model=list[SaleResponseSchema])
def get_all_sales(
    skip: int = 0,
    limit: int = 100,
    service: ISalesService = Depends(get_sales_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Obtiene todas las ventas registradas."""
    return service.get_all(skip=skip, limit=limit)


@router.get("/{sale_id}", response_model=SaleResponseSchema)
def get_sale_by_id(
    sale_id: int,
    service: ISalesService = Depends(get_sales_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """Obtiene una venta por su ID."""
    return service.get_by_id(sale_id)


@router.post("", status_code=201, response_model=SaleResponseSchema)
def create_sale(
    sale: SaleCreateSchema,
    service: ISalesService = Depends(get_sales_service),
    current_user: UserDTO = Depends(role_master_or_admin),
):
    """
    Registra una nueva venta.
    Aplica las reglas de negocio:
    - La propiedad no puede estar ya vendida
    - La propiedad debe estar listada en el catálogo
    - Se requieren lead, vendedor, comprador y propiedad
    """
    sale_dto = SaleDTO(**sale.model_dump(exclude_none=True))
    return service.create(sale_dto)
