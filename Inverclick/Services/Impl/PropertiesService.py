from Repositories.IPropertiesRepository import IPropertiesRepository
from Repositories.IConstructorasRepository import IConstructorasRepository
from Models.real_estate import RealEstateDTO
from Models.users import UserDTO
from Services.IPropertiesService import IPropertiesService
from Utils.HttpResponses.propertyHttpResponses import PropertyHttpResponses


class PropertiesService(IPropertiesService):
    """
    Servicio con lógica de negocio pesada para la gestión de propiedades.
    Centraliza validaciones de:
    - Unicidad de nombre (CA2)
    - Unicidad de dirección (CA2)
    - Campos obligatorios: precio y constructora (CA2)
    - Verificación de existencia de la constructora asociada
    - Control de permisos por constructora (CRUD restringido)
    """

    def __init__(
        self,
        repository: IPropertiesRepository,
        constructoras_repository: IConstructorasRepository,
        http_responses: PropertyHttpResponses
    ):
        self.repository = repository
        self.constructoras_repository = constructoras_repository
        self.http_responses = http_responses

    def _check_constructora_permission(self, current_user: UserDTO | None, target_constructora_id: int | None):
        """Verifica que si el usuario tiene rol Constructora, pertenezca a la misma constructora objetivo."""
        if current_user and getattr(current_user, 'role', None) == "Constructora":
            user_company_id = getattr(current_user, 'id_constructionCompany', None)
            if not user_company_id or user_company_id != target_constructora_id:
                raise self.http_responses.error_forbidden_constructora_access()

    def get_by_id(self, property_id: int, current_user: UserDTO | None = None) -> RealEstateDTO | None:
        prop = self.repository.get_by_id(property_id)
        if prop is None:
            raise self.http_responses.error_not_found()
        self._check_constructora_permission(current_user, prop.id_constructionCompany)
        return prop

    def get_all(self, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[RealEstateDTO]:
        if current_user and getattr(current_user, 'role', None) == "Constructora":
            user_company_id = getattr(current_user, 'id_constructionCompany', None)
            if not user_company_id:
                raise self.http_responses.error_forbidden_constructora_access()
            return self.repository.get_by_constructora_id(user_company_id, skip, limit)
        return self.repository.get_all(skip, limit)

    def get_by_constructora(self, constructora_id: int, skip: int = 0, limit: int = 100, current_user: UserDTO | None = None) -> list[RealEstateDTO]:
        """Obtiene las propiedades de una constructora específica."""
        self._check_constructora_permission(current_user, constructora_id)
        return self.repository.get_by_constructora_id(constructora_id, skip, limit)

    def create(self, propertyDTO: RealEstateDTO, current_user: UserDTO | None = None) -> RealEstateDTO:
        if current_user and getattr(current_user, 'role', None) == "Constructora":
            user_company_id = getattr(current_user, 'id_constructionCompany', None)
            if not user_company_id:
                raise self.http_responses.error_forbidden_constructora_access()
            if propertyDTO.id_constructionCompany is not None and propertyDTO.id_constructionCompany != user_company_id:
                raise self.http_responses.error_forbidden_constructora_access()
            propertyDTO.id_constructionCompany = user_company_id

        # CA2: Campos obligatorios — precio
        if propertyDTO.price is None:
            raise self.http_responses.error_missing_price()

        # CA2: Campos obligatorios — constructora asociada
        if propertyDTO.id_constructionCompany is None:
            raise self.http_responses.error_missing_constructora()

        # Verificar que la constructora asociada exista
        constructora = self.constructoras_repository.get_by_id(propertyDTO.id_constructionCompany)
        if constructora is None:
            raise self.http_responses.error_constructora_not_found()

        # CA2: Unicidad de nombre — no puede haber dos propiedades con el mismo nombre
        if propertyDTO.name and self.repository.get_by_name(propertyDTO.name) is not None:
            raise self.http_responses.error_name_already_exists()

        # CA2: Unicidad de dirección — no puede haber dos propiedades con la misma dirección exacta
        if propertyDTO.address and self.repository.get_by_address(propertyDTO.address) is not None:
            raise self.http_responses.error_address_already_exists()

        result = self.repository.create(propertyDTO)
        if result is None:
            raise self.http_responses.error_not_created()
        return result

    def update(self, property_id: int, propertyDTO: RealEstateDTO, current_user: UserDTO | None = None) -> RealEstateDTO | None:
        existing = self.repository.get_by_id(property_id)
        if existing is None:
            raise self.http_responses.error_not_found()

        self._check_constructora_permission(current_user, existing.id_constructionCompany)

        # Bloquear edición si la propiedad ya fue vendida
        if existing.sales_status:
            raise self.http_responses.error_already_sold()

        # Validar unicidad de nombre si se está cambiando
        new_name = getattr(propertyDTO, 'name', None)
        if new_name and new_name != existing.name:
            if self.repository.get_by_name(new_name) is not None:
                raise self.http_responses.error_name_already_exists()

        # Validar unicidad de dirección si se está cambiando
        new_address = getattr(propertyDTO, 'address', None)
        if new_address and new_address != existing.address:
            if self.repository.get_by_address(new_address) is not None:
                raise self.http_responses.error_address_already_exists()

        # Verificar constructora si se cambia
        new_constructora_id = getattr(propertyDTO, 'id_constructionCompany', None)
        if new_constructora_id and new_constructora_id != existing.id_constructionCompany:
            if current_user and getattr(current_user, 'role', None) == "Constructora":
                raise self.http_responses.error_forbidden_constructora_access()
            if self.constructoras_repository.get_by_id(new_constructora_id) is None:
                raise self.http_responses.error_constructora_not_found()

        result = self.repository.update(property_id, propertyDTO)
        if result is None:
            raise self.http_responses.error_not_updated()
        return result

    def delete(self, property_id: int, current_user: UserDTO | None = None) -> bool:
        existing = self.repository.get_by_id(property_id)
        if existing is None:
            raise self.http_responses.error_not_found()

        self._check_constructora_permission(current_user, existing.id_constructionCompany)

        # Bloquear eliminación si la propiedad ya fue vendida
        if existing.sales_status:
            raise self.http_responses.error_already_sold()

        success = self.repository.delete(property_id)
        if not success:
            raise self.http_responses.error_not_deleted()
        return success

    def get_favorites(self, user_id: int, skip: int = 0, limit: int = 100) -> list[RealEstateDTO]:
        return self.repository.get_favorites_by_user_id(user_id=user_id, skip=skip, limit=limit)

