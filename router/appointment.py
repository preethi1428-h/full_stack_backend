from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.database import get_db
from modules.appointment_mod import Appointment
from schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])



@router.post("/", response_model=AppointmentResponse)
def create_appointment(app_data: AppointmentCreate, db: Session = Depends(get_db)):

    existing = db.query(Appointment).filter(
        Appointment.provider_id == app_data.provider_id,
        Appointment.date == app_data.date,
        Appointment.time == app_data.time
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="This time slot already booked")

    new_app = Appointment(
        name=app_data.name,
        email=app_data.email,
        phone=app_data.phone,
        date=app_data.date,
        time=app_data.time,
        service_id=app_data.service_id,
        provider_id=app_data.provider_id,
        additional=app_data.additional,
        user_id=app_data.user_id
    )

    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    return new_app


# GET ALL APPOINTMENTS

@router.get("/", response_model=list[AppointmentResponse])
def get_all_appointments(db: Session = Depends(get_db)):

    appointments = (
        db.query(Appointment)
        .options(
            joinedload(Appointment.provider),
            joinedload(Appointment.service)
        )
        .all()
    )

    return appointments


# GET ONE APPOINTMENT
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_one_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = (
        db.query(Appointment)
        .options(
            joinedload(Appointment.provider),
            joinedload(Appointment.service)
        )
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment

# GET APPOINTMENTS FOR USER

@router.get("/my/{user_id}", response_model=list[AppointmentResponse])
def get_my_appointments(user_id: int, db: Session = Depends(get_db)):

    appointments = (
        db.query(Appointment)
        .options(
            joinedload(Appointment.provider),
            joinedload(Appointment.service)
        )
        .filter(Appointment.user_id == user_id)
        .all()
    )

    return appointments


# GET APPOINTMENTS FOR PROVIDER

@router.get("/provider/{provider_id}", response_model=list[AppointmentResponse])
def get_appointments_for_provider(provider_id: int, db: Session = Depends(get_db)):

    appointments = (
        db.query(Appointment)
        .options(
            joinedload(Appointment.provider),
            joinedload(Appointment.service)
        )
        .filter(Appointment.provider_id == provider_id)
        .all()
    )

    return appointments


# ACCEPT APPOINTMENT

@router.patch("/{appointment_id}/provider/accepted")
def accept_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "Accepted"
    db.commit()

    return {"message": "Appointment Accepted"}


# REJECT APPOINTMENT

@router.patch("/{appointment_id}/provider/rejected")
def reject_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "Rejected"
    db.commit()

    return {"message": "Appointment Rejected"}


# DELETE APPOINTMENT

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment Deleted Successfully"}