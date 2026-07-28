from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Services.CountryService import CountryService
from Repositories.CountryRepository import CountryRepository 
from Repositories.PrefixRepository import PrefixRepository
from Repositories.database import get_db
from Schemas.CountrySchema import CountryCreate, CountryUpdate, CountryOut

router = APIRouter(prefix="/country", tags=["Country"])

def get_country_service(db: Session = Depends(get_db)) -> CountryService:
    country_repository = CountryRepository(db)
    prefix_repository = PrefixRepository(db)
    return CountryService(country_repository, prefix_repository)


@router.get("/", response_model=list[CountryOut])
def get_all_countries(skip: int = 0, limit: int = 100, service: CountryService = Depends(get_country_service)):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{country_id}", response_model=CountryOut)
def get_country_by_id(country_id: int, service: CountryService = Depends(get_country_service)):
    try:
        return service.get_by_id(country_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/iso/{iso}", response_model=CountryOut)
def get_country_by_iso(iso: str, service: CountryService = Depends(get_country_service)):
    try:
        return service.get_by_iso(iso)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/name/{name}", response_model=CountryOut)
def get_country_by_name(name: str, service: CountryService = Depends(get_country_service)):
    try:
        return service.get_by_name(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.post("/", response_model=CountryOut, status_code=201)
def create_country(data: CountryCreate, service: CountryService = Depends(get_country_service)):
    try:
        return service.create(data.name, data.iso, data.prefix_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    

@router.patch("/{country_id}", response_model=CountryOut)
def update_country(country_id: int, data: CountryUpdate, service: CountryService = Depends(get_country_service)):
    try:
        return service.update(country_id, data.name, data.iso, data.prefix_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.delete("/{country_id}", status_code=200)
def delete_country(country_id: int, service: CountryService = Depends(get_country_service)):
    try:
        service.delete(country_id)
        return {"message": f"Country con ID {country_id} eliminado exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))