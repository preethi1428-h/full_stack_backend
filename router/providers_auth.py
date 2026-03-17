from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from modules.provider_mod import Provider
from schemas.provider import ProviderCreate, ProviderLogin, ProviderResponse


router = APIRouter(prefix="/provider", tags=["Provider Login"])


# 🔹 REGISTER
@router.post("/register", response_model=ProviderResponse)
def register_provider(data: ProviderCreate, db: Session = Depends(get_db)):


    existing = db.query(Provider).filter(Provider.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")


    new_provider = Provider(
        name=data.name,
        email=data.email,
        specialization=data.specialization,
        password=data.password,
        service_id=data.service_id
    )

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return new_provider



# 🔹 LOGIN
@router.post("/login")
def login_provider(data: ProviderLogin, db: Session = Depends(get_db)):

    provider = db.query(Provider).filter(Provider.email == data.email).first()

    if not provider or provider.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login Successful",
        "id": provider.id,
        "name": provider.name,
        "email": provider.email,
        "specialization": provider.specialization
    }

@router.get("/by-service/{service_id}")
def get_providers_by_service(service_id: int, db: Session = Depends(get_db)):
    providers = db.query(Provider).filter(
        Provider.service_id == service_id
    ).all()
    return providers

