from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Services.UsersService import UsersService
from Repositories.UsersRepository import UsersRepository
from Repositories.CountryRepository import CountryRepository
from Repositories.database import get_db
from Schemas.UsersSchema import UsersCreate, UsersUpdate, UsersOut  

router = APIRouter(prefix="/users", tags=["Users"])

def get_users_service(db: Session = Depends(get_db)) -> UsersService:
    users_repository = UsersRepository(db)
    country_repository = CountryRepository(db)
    return UsersService(users_repository, country_repository)

@router.get("/", response_model=list[UsersOut])
def get_all_users(skip: int = 0, limit: int = 100, service: UsersService = Depends(get_users_service)):
    return service.get_all(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UsersOut)
def get_user_by_id(user_id: int, service: UsersService = Depends(get_users_service)):
    try:
        return service.get_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/email/{email}", response_model=UsersOut)
def get_user_by_email(email: str, service: UsersService = Depends(get_users_service)):      
    try:
        return service.get_by_email(email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/id_number/{id_number}", response_model=UsersOut)
def get_user_by_id_number(id_number: str, service: UsersService = Depends(get_users_service)):
    try:
        return service.get_by_id_number(id_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=UsersOut, status_code=201)
def create_user(data: UsersCreate, service: UsersService = Depends(get_users_service)):
    try:
        return service.create(
            name=data.name,
            lastname=data.lastname,
            address=data.address,
            zip_code=data.zip_code,
            email=data.email,
            residence_city=data.residence_city,
            country_id=data.country_id,
            cell_number=data.cell_number,
            taxes=data.taxes,
            income=data.income,
            job=data.job,
            outcome=data.outcome,
            id_number=data.id_number,
            description=data.description
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.patch("/{user_id}", response_model=UsersOut)
def update_user(user_id: int, data: UsersUpdate, service: UsersService = Depends(get_users_service)):
    try:
        return service.update(
            user_id=user_id,
            name=data.name,
            lastname=data.lastname,
            address=data.address,
            zip_code=data.zip_code,
            email=data.email,
            residence_city=data.residence_city,
            country_id=data.country_id,
            cell_number=data.cell_number,
            taxes=data.taxes,
            income=data.income,
            job=data.job,
            outcome=data.outcome,
            id_number=data.id_number,
            description=data.description
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", status_code=200)
def delete_user(user_id: int, service: UsersService = Depends(get_users_service)):
    try:
        service.delete(user_id)
        return {"message": f"Usuario con ID {user_id} eliminado correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))