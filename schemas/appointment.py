from pydantic import BaseModel
from typing import Optional

from schemas.services_schemas import ServiceResponse
from schemas.provider import ProviderResponse


class AppointmentCreate(BaseModel):
    name: str
    phone: str
    email: str
    date: str
    time: str
    service_id: int
    provider_id: int
    additional: Optional[str] = None
    user_id: int


class AppointmentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    date: str
    time: str
    additional: Optional[str] = None
    status: str
    user_id: int
    service_id: int
    provider_id: int

    service: Optional[ServiceResponse] = None
    provider: Optional[ProviderResponse] = None

    model_config = {"from_attributes": True}

    