from Repositories.ILeadsRepository import ILeadsRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Repositories.IPropertiesRepository import IPropertiesRepository
from Repositories.IConstructorasRepository import IConstructorasRepository
from Models.leads import LeadDTO
from Models.users import UserDTO
from Services.ILeadsService import ILeadsService
from Utils.HttpResponses.leadHttpResponses import LeadHttpResponses


class LeadsService(ILeadsService):
    """
    Servicio con lógica de negocio para la gestión de leads y favoritos.
    - Soporta la creación y alternado de favoritos por usuario.
    - Asocia automáticamente la constructora según la propiedad.
    - Filtra leads por pertenencia a constructora o usuario según rol.
    """

    def __init__(
        self,
        repository: ILeadsRepository,
        users_repository: IUsuariosRepository,
        properties_repository: IPropertiesRepository,
        http_responses: LeadHttpResponses,
        constructoras_repository: IConstructorasRepository | None = None
    ):
        self.repository = repository
        self.users_repository = users_repository
        self.properties_repository = properties_repository
        self.http_responses = http_responses
        self.constructoras_repository = constructoras_repository

    def _check_lead_permission(self, lead: LeadDTO, current_user: UserDTO | None):
        if not current_user:
            return
        role = getattr(current_user, 'role', None)
        if role == "Constructora":
            user_company_id = getattr(current_user, 'id_constructionCompany', None)
            if not user_company_id or lead.id_constructionCompany != user_company_id:
                raise self.http_responses.error_forbidden_lead_access()
        elif role == "Usuario":
            if lead.id_user != current_user.id:
                raise self.http_responses.error_forbidden_lead_access()

    def get_by_id(self, lead_id: int, current_user: UserDTO | None = None) -> LeadDTO | None:
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            raise self.http_responses.error_not_found()
        self._check_lead_permission(lead, current_user)
        return lead

    def get_all(self, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[LeadDTO]:
        if current_user:
            role = getattr(current_user, 'role', None)
            if role == "Constructora":
                user_company_id = getattr(current_user, 'id_constructionCompany', None)
                if not user_company_id:
                    raise self.http_responses.error_forbidden_lead_access()
                return self.repository.get_by_constructora_id(user_company_id, skip, limit)
            elif role == "Usuario":
                return self.repository.get_by_user_id(current_user.id, skip, limit)
        return self.repository.get_all(skip, limit)

    def get_favorites(self, current_user: UserDTO, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        return self.repository.get_favorites_by_user_id(current_user.id, skip, limit)

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[LeadDTO]:
        if current_user and getattr(current_user, 'role', None) == "Usuario" and current_user.id != user_id:
            raise self.http_responses.error_forbidden_lead_access()
        return self.repository.get_by_user_id(user_id, skip, limit)

    def get_by_property(self, real_estate_id: int, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[LeadDTO]:
        if current_user and getattr(current_user, 'role', None) == "Constructora":
            prop = self.properties_repository.get_by_id(real_estate_id)
            if prop and prop.id_constructionCompany != getattr(current_user, 'id_constructionCompany', None):
                raise self.http_responses.error_forbidden_lead_access()
        return self.repository.get_by_real_estate_id(real_estate_id, skip, limit)

    def toggle_favorite(self, leadDTO: LeadDTO, current_user: UserDTO) -> LeadDTO:
        user_id = current_user.id
        leadDTO.id_user = user_id
        real_estate_id = leadDTO.id_real_state if leadDTO.id_real_state and leadDTO.id_real_state > 0 else None
        constructora_id = leadDTO.id_constructionCompany if leadDTO.id_constructionCompany and leadDTO.id_constructionCompany > 0 else None
        leadDTO.id_real_state = real_estate_id
        leadDTO.id_constructionCompany = constructora_id

        if real_estate_id is None and constructora_id is None:
            raise self.http_responses.error_missing_target()

        if real_estate_id is not None:
            prop = self.properties_repository.get_by_id(real_estate_id)
            if prop is None:
                raise self.http_responses.error_property_not_found()
            constructora_id = prop.id_constructionCompany
            leadDTO.id_constructionCompany = constructora_id
        elif constructora_id is not None:
            if self.constructoras_repository:
                c = self.constructoras_repository.get_by_id(constructora_id)
                if c is None:
                    raise self.http_responses.error_constructora_not_found()

        existing = self.repository.get_by_user_and_target(
            user_id=user_id,
            real_estate_id=real_estate_id,
            constructora_id=constructora_id if real_estate_id is None else None
        )

        if existing:
            new_status = not existing.is_favorite
            updated = self.repository.update(existing.id, {"is_favorite": new_status})
            if updated is None:
                raise self.http_responses.error_not_created()
            return updated
        else:
            leadDTO.is_favorite = True
            result = self.repository.create(leadDTO)
            if result is None:
                raise self.http_responses.error_not_created()
            return result

    def create(self, leadDTO: LeadDTO, current_user: UserDTO | None = None) -> LeadDTO:
        if current_user:
            return self.toggle_favorite(leadDTO, current_user)

        if not leadDTO.id_user:
            raise self.http_responses.error_user_not_found()
        user = self.users_repository.get_by_id(leadDTO.id_user)
        if user is None:
            raise self.http_responses.error_user_not_found()

        if leadDTO.id_real_state is not None:
            prop = self.properties_repository.get_by_id(leadDTO.id_real_state)
            if prop is None:
                raise self.http_responses.error_property_not_found()
            if leadDTO.id_constructionCompany is None:
                leadDTO.id_constructionCompany = prop.id_constructionCompany

        result = self.repository.create(leadDTO)
        if result is None:
            raise self.http_responses.error_not_created()
        return result

    def delete(self, lead_id: int, current_user: UserDTO | None = None) -> bool:
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            raise self.http_responses.error_not_found()

        self._check_lead_permission(lead, current_user)

        success = self.repository.delete(lead_id)
        if not success:
            raise self.http_responses.error_not_deleted()
        return success

