from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from modules.provider_mod import Provider
from schemas.provider import ProviderCreate, ProviderResponse

router = APIRouter(prefix="/providers", tags=["Providers"])

# CREATE PROVIDER
@router.post("/", response_model=ProviderResponse)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    new_provider = Provider(
        name=provider.name,
        specialization=provider.specialization,
        service_id=provider.service_id
    )
    
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider


# GET ALL PROVIDERS
@router.get("/", response_model=list[ProviderResponse])
def get_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()


# GET PROVIDERS BY SERVICE (IMPORTANT FOR AUTO DROPDOWN)
@router.get("/service/{service_id}", response_model=list[ProviderResponse])
def get_providers_by_service(service_id: int, db: Session = Depends(get_db)):
    providers = db.query(Provider).filter(Provider.service_id == service_id).all()

    if not providers:
        raise HTTPException(status_code=404, detail="No providers found for this service")

    return providers


# GET ONE PROVIDER
@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider


# DELETE PROVIDER
@router.delete("/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()

    return {"message": "Provider deleted successfully"}
