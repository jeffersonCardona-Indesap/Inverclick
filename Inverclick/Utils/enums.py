from enum import Enum

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class IdentificationTypeEnum(str, Enum):
    CC = "CC"
    CE = "CE"
    PAS = "PAS"
    NIT = "NIT"
    PEP = "PEP"

class PropertyStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class SalesStatusEnum(str, Enum):
    AVAILABLE = "available"
    SOLD = "sold"

class AuditActionEnum(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SALE = "SALE"
