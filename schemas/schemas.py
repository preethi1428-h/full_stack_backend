from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    model_config = {"from_attributes": True}




   