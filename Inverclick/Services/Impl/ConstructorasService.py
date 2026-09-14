from Repositories.IConstructorasRepository import IConstructorasRepository
from Models.constructoras import ConstructionCompanyDTO
from Services.IConstructorasService import IConstructorasService
from Utils.HttpResponses.constructoraHttpResponses import ConstructoraHttpResponses


class ConstructorasService(IConstructorasService):
    """
    Servicio con lógica de negocio para la gestión de constructoras.
    Centraliza validaciones de unicidad de NIT y nombre.
    """

    def __init__(self, repository: IConstructorasRepository, http_responses: ConstructoraHttpResponses):
        self.repository = repository
        self.http_responses = http_responses

    def get_by_id(self, company_id: int) -> ConstructionCompanyDTO | None:
        company = self.repository.get_by_id(company_id)
        if company is None:
            raise self.http_responses.error_not_found()
        return company

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ConstructionCompanyDTO]:
        return self.repository.get_all(skip, limit)

    def create(self, companyDTO: ConstructionCompanyDTO) -> ConstructionCompanyDTO:
        # Validar unicidad de NIT
        if companyDTO.nit and self.repository.get_by_nit(companyDTO.nit) is not None:
            raise self.http_responses.error_nit_already_exists()

        # Validar unicidad de Nombre
        if companyDTO.Nombre and self.repository.get_by_nombre(companyDTO.Nombre) is not None:
            raise self.http_responses.error_nombre_already_exists()

        result = self.repository.create(companyDTO)
        if result is None:
            raise self.http_responses.error_not_created()
        return result

    def update(self, company_id: int, companyDTO: ConstructionCompanyDTO) -> ConstructionCompanyDTO | None:
        # Verificar que la constructora exista
        existing = self.repository.get_by_id(company_id)
        if existing is None:
            raise self.http_responses.error_not_found()

        # Validar unicidad de NIT si se está cambiando
        if companyDTO.nit and companyDTO.nit != existing.nit:
            if self.repository.get_by_nit(companyDTO.nit) is not None:
                raise self.http_responses.error_nit_already_exists()

        # Validar unicidad de Nombre si se está cambiando
        if companyDTO.Nombre and companyDTO.Nombre != existing.Nombre:
            if self.repository.get_by_nombre(companyDTO.Nombre) is not None:
                raise self.http_responses.error_nombre_already_exists()

        result = self.repository.update(company_id, companyDTO)
        if result is None:
            raise self.http_responses.error_not_updated()
        return result

    def delete(self, company_id: int) -> bool:
        success = self.repository.delete(company_id)
        if not success:
            raise self.http_responses.error_not_deleted()
        return success
