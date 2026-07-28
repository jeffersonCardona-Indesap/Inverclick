from Repositories.UsersRepository import UsersRepository
from Repositories.CountryRepository import CountryRepository
from Models.Users import Users

class UsersService:

    def __init__(self, users_repository: UsersRepository, country_repository: CountryRepository):
        self.users_repository = users_repository
        self.country_repository = country_repository

    def get_by_id(self, user_id: int) -> Users | None:
        user = self.users_repository.get_by_id(user_id)
        if user is None:
            raise ValueError(f"Usuario con ID {user_id} no encontrado.")
        return user

    def get_by_email(self, email: str) -> Users | None:
        user = self.users_repository.get_by_email(email)
        if user is None:
            raise ValueError(f"Usuario con correo electrónico {email} no encontrado.")
        return user

    def get_by_id_number(self, id_number: str) -> Users | None:
        user = self.users_repository.get_by_id_number(id_number)
        if user is None:
            raise ValueError(f"Usuario con número de identificación {id_number} no encontrado.")
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Users]:
        return self.users_repository.get_all(skip, limit)

    def create(
        self,
        name: str,
        lastname: str,
        address: str,
        zip_code: str,
        email: str,
        residence_city: str,
        country_id: int,
        cell_number: str,
        taxes: float,
        income: float,
        job: str,
        outcome: float,
        id_number: str,
        description: str,
    ) -> Users:

        name = name.strip().title()
        lastname = lastname.strip().title()
        residence_city = residence_city.strip().title()
        job = job.strip().title()
        
        existing_user_email = self.users_repository.get_by_email(email)
        if existing_user_email is not None:
            raise ValueError(f"Usuario con correo electrónico {email} ya existe.")

        existing_user_id_number = self.users_repository.get_by_id_number(id_number)
        if existing_user_id_number is not None:
            raise ValueError(f"Usuario con número de identificación {id_number} ya existe.")

        existing_country = self.country_repository.get_by_id(country_id)
        if existing_country is None:
            raise ValueError(f"Country con ID {country_id} no encontrado.")

        new_user = Users(
            name=name,
            lastname=lastname,
            address=address,
            zip_code=zip_code,
            email=email,
            residence_city=residence_city,
            country_id=country_id,
            cell_number=cell_number,
            taxes=taxes,
            income=income,
            job=job,
            outcome=outcome,
            id_number=id_number,
            description=description
        )
        return self.users_repository.create(new_user)   

    def update(
        self,
        user_id: int,
        name: str,
        lastname: str,
        address: str,
        zip_code: str,
        email: str,
        residence_city: str,
        country_id: int,
        cell_number: str,
        taxes: float,
        income: float,
        job: str,
        outcome: float,
        id_number: str,
        description: str,
    ) -> Users | None:

        name = name.strip().title()
        lastname = lastname.strip().title()
        residence_city = residence_city.strip().title()
        job = job.strip().title()
        
        existing_user_email = self.users_repository.get_by_email(email)
        if existing_user_email is not None and existing_user_email.id != user_id:
            raise ValueError(f"Usuario con correo electrónico {email} ya existe.")

        existing_user_id_number = self.users_repository.get_by_id_number(id_number)
        if existing_user_id_number is not None and existing_user_id_number.id != user_id:
            raise ValueError(f"Usuario con número de identificación {id_number} ya existe.")

        existing_country = self.country_repository.get_by_id(country_id)
        if existing_country is None:
            raise ValueError(f"Country con ID {country_id} no encontrado.")

        updated_user = self.users_repository.update(
            user_id, name, lastname, address, zip_code, email,
            residence_city, country_id, cell_number, taxes,
            income, job, outcome, id_number, description
        )
        if updated_user is None:
            raise ValueError(f"Usuario con ID {user_id} no encontrado.")
        return updated_user

    def delete(self, user_id: int) -> None:
        deleted = self.users_repository.delete(user_id)
        if not deleted:
            raise ValueError(f"Usuario con ID {user_id} no encontrado.")