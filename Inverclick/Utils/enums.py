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

class RoleEnum(str, Enum):
    ADMIN = "Admin"
    MASTER = "Master"
    CONSTRUCTORA = "Constructora"
    VENTAS = "Ventas"
    CLIENTE = "Cliente"
