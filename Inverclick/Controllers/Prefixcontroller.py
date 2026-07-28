from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Services.PrefixService import PrefixService
from Repositories.PrefixRepository import PrefixRepository
from Repositories.database import get_db
from Schemas.PrefixSchema import PrefixCreate, PrefixUpdate, PrefixOut

router = APIRouter(prefix="/prefix", tags=["Prefix"])


def get_prefix_service(db: Session = Depends(get_db)) -> PrefixService:
    repository = PrefixRepository(db)
    return PrefixService(repository)


@router.get("/", response_model=list[PrefixOut])
def get_all_prefixes(skip: int = 0, limit: int = 100, service: PrefixService = Depends(get_prefix_service)):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{prefix_id}", response_model=PrefixOut)
def get_prefix_by_id(prefix_id: int, service: PrefixService = Depends(get_prefix_service)):
    try:
        return service.get_by_id(prefix_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/code/{code}", response_model=PrefixOut)
def get_prefix_by_code(code: str, service: PrefixService = Depends(get_prefix_service)):
    try:
        return service.get_by_code(code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=PrefixOut, status_code=201)
def create_prefix(data: PrefixCreate, service: PrefixService = Depends(get_prefix_service)):
    try:
        return service.create(data.code)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{prefix_id}", response_model=PrefixOut)
def update_prefix(prefix_id: int, data: PrefixUpdate, service: PrefixService = Depends(get_prefix_service)):
    try:
        return service.update(prefix_id, data.code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{prefix_id}", status_code=200)
def delete_prefix(prefix_id: int, service: PrefixService = Depends(get_prefix_service)):
    try:
        service.delete(prefix_id)
        return {"message": "Prefijo eliminado correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))