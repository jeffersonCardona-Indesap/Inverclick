from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UsersCreate(BaseModel):
    name: str = Field(..., min_length=1, description="El nombre del usuario debe tener al menos 1 carácter.")
    lastname: str = Field(..., min_length=1, description="El apellido del usuario debe tener al menos 1 carácter.")
    address: str = Field(..., min_length=1, description="La dirección del usuario debe tener al menos 1 carácter.")
    zip_code: str = Field(..., min_length=1, description="El código postal del usuario debe tener al menos 1 carácter.")
    email: EmailStr = Field(..., description="El correo electrónico del usuario es obligatorio.")
    residence_city: str = Field(..., min_length=1, description="La ciudad de residencia del usuario debe tener al menos 1 carácter.")
    country_id: int = Field(..., description="El ID del país del usuario es obligatorio.")
    cell_number: float = Field(..., description="El número de celular del usuario es obligatorio.")
    taxes: float = Field(..., description="Los impuestos del usuario son obligatorios.")
    income: float = Field(..., description="El ingreso del usuario es obligatorio.")
    job: str = Field(..., min_length=1, description="El trabajo del usuario debe tener al menos 1 carácter.")
    outcome: float = Field(..., description="El resultado del usuario es obligatorio.")
    id_number: str = Field(..., min_length=1, description="El número de identificación del usuario debe tener al menos 1 carácter.")
    description: str = Field(..., min_length=1, description="La descripción del usuario debe tener al menos 1 carácter.")

class UsersUpdate(BaseModel):
    name: str = Field(..., min_length=1, description="El nombre del usuario debe tener al menos 1 carácter.")
    lastname: str = Field(..., min_length=1, description="El apellido del usuario debe tener al menos 1 carácter.")
    address: str = Field(..., min_length=1, description="La dirección del usuario debe tener al menos 1 carácter.")
    zip_code: str = Field(..., min_length=1, description="El código postal del usuario debe tener al menos 1 carácter.")
    email: EmailStr = Field(..., description="El correo electrónico del usuario es obligatorio.")
    residence_city: str = Field(..., min_length=1, description="La ciudad de residencia del usuario debe tener al menos 1 carácter.")
    country_id: int = Field(..., description="El ID del país del usuario es obligatorio.")
    cell_number: float = Field(..., description="El número de celular del usuario es obligatorio.")
    taxes: float = Field(..., description="Los impuestos del usuario son obligatorios.")
    income: float = Field(..., description="El ingreso del usuario es obligatorio.")
    job: str = Field(..., min_length=1, description="El trabajo del usuario debe tener al menos 1 carácter.")
    outcome: float = Field(..., description="El resultado del usuario es obligatorio.")
    id_number: str = Field(..., min_length=1, description="El número de identificación del usuario debe tener al menos 1 carácter.")
    description: str = Field(..., min_length=1, description="La descripción del usuario debe tener al menos 1 carácter.")

class UsersOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    lastname: str
    address: str
    zip_code: str
    email: EmailStr
    residence_city: str
    country_id: int 
    cell_number: float
    taxes: float
    income: float
    job: str
    outcome: float
    id_number: str
    description: str