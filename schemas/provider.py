from pydantic import BaseModel
from typing import Optional

class ProviderCreate(BaseModel):
    name: str
    email: str
    specialization: str
    password: str
    service_id: Optional[int] = None

class ProviderLogin(BaseModel):
    email: str
    password: str

class ProviderResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]=None
    specialization: str
    service_id: Optional[int] = None

    model_config = {"from_attributes": True}

