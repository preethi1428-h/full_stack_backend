from pydantic import BaseModel

class ContactCreate(BaseModel):
    name: str
    email: str
    message: str


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str

    model_config = {"from_attributes": True}
