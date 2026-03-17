from pydantic import BaseModel

class ServiceCreate(BaseModel):
    title: str



class ServiceUpdate(BaseModel):
    title: str | None = None


class ServiceResponse(BaseModel):
    id: int
    title: str
    
    model_config = {
        "from_attributes": True
    }

