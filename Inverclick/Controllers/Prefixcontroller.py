# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from Models.prefix import Prefix
# pyrefly: ignore [missing-import]
from Services.IPrefixservice import IPrefixService
# pyrefly: ignore [missing-import]
from Services.Impl.prefixService import PrefixService
# pyrefly: ignore [missing-import]
from Repositories.PrefixRepository import PrefixRepository
from Repositories.database import get_db
from Utils.auth_middleware import get_current_user

router = APIRouter(prefix="/prefix", tags=["Prefix"])

def get_prefix_service(db: Session = Depends(get_db)) -> IPrefixService:
    repository = PrefixRepository(db)
    return PrefixService(repository)

@router.get("/{prefix_id}")
def get_prefix_by_id(
    prefix_id: int, 
    service: IPrefixService = Depends(get_prefix_service),
    current_user = Depends(get_current_user)
):
    try:
        return service.get_by_id(prefix_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def get_all_prefixes(
    skip: int = 0, 
    limit: int = 100, 
    service: IPrefixService = Depends(get_prefix_service),
    current_user = Depends(get_current_user)
):
    try:
        return service.get_all(skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
