from pydantic import BaseModel, ConfigDict, Field


class PrefixCreate(BaseModel):
    code: str = Field(..., min_length=1,description="El campo no puede quedar vacio")


class PrefixUpdate(BaseModel):
    code: str = Field(..., min_length=1, description="El campo no puede quedar vacio")


class PrefixOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str