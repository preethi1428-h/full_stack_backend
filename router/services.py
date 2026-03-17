from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from modules.models import Service 
from schemas.services_schemas import ServiceCreate, ServiceUpdate, ServiceResponse


router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(
        title=service.title
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service



@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services



@router.get("/{service_id}", response_model=ServiceResponse)
def get_single_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, service_data: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if service_data.title is not None:
        service.title = service_data.title
    if service_data.description is not None:
        service.description = service_data.description
    if service_data.icon is not None:
        service.icon = service_data.icon

    db.commit()
    db.refresh(service)

    return service


@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully"}

