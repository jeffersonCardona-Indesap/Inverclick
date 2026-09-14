from Repositories.ILeadsRepository import ILeadsRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Repositories.IPropertiesRepository import IPropertiesRepository
from Models.leads import LeadDTO
from Services.ILeadsService import ILeadsService
from Utils.HttpResponses.leadHttpResponses import LeadHttpResponses


class LeadsService(ILeadsService):
    """
    Servicio con lógica de negocio para la gestión de leads.
    Valida existencia de usuario y propiedad referenciados.
    """

    def __init__(
        self,
        repository: ILeadsRepository,
        users_repository: IUsuariosRepository,
        properties_repository: IPropertiesRepository,
        http_responses: LeadHttpResponses
    ):
        self.repository = repository
        self.users_repository = users_repository
        self.properties_repository = properties_repository
        self.http_responses = http_responses

    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            raise self.http_responses.error_not_found()
        return lead

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        return self.repository.get_all(skip, limit)

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        return self.repository.get_by_user_id(user_id, skip, limit)

    def get_by_property(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        return self.repository.get_by_real_estate_id(real_estate_id, skip, limit)

    def create(self, leadDTO: LeadDTO) -> LeadDTO:
        # Validar que el usuario referenciado exista
        user = self.users_repository.get_by_id(leadDTO.id_user)
        if user is None:
            raise self.http_responses.error_user_not_found()

        # Validar que la propiedad referenciada exista
        prop = self.properties_repository.get_by_id(leadDTO.id_real_state)
        if prop is None:
            raise self.http_responses.error_property_not_found()

        result = self.repository.create(leadDTO)
        if result is None:
            raise self.http_responses.error_not_created()
        return result

    def delete(self, lead_id: int) -> bool:
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            raise self.http_responses.error_not_found()

        success = self.repository.delete(lead_id)
        if not success:
            raise self.http_responses.error_not_deleted()
        return success
