from pydantic import BaseModel, ConfigDict, Field

class CountryCreate(BaseModel):
    name: str = Field(..., min_length=1)
    iso: str = Field(..., min_length=1)
    prefix_id: int

class CountryUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    iso: str = Field(..., min_length=1)
    prefix_id: int

class CountryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    iso: str
    prefix_id: int
    
