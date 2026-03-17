from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from modules.contact_mod import Contact
from schemas.contact_schema import ContactCreate, ContactResponse

router = APIRouter(prefix="/contact", tags=["Contact"])

# USER SUBMITS CONTACT FORM
@router.post("/", response_model=ContactResponse)
def submit_contact(data: ContactCreate, db: Session = Depends(get_db)):
    new_msg = Contact(
        name=data.name,
        email=data.email,
        message=data.message
    )

    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    return new_msg


# ADMIN – VIEW ALL CONTACT MESSAGES
@router.get("/", response_model=list[ContactResponse])
def get_messages(db: Session = Depends(get_db)):
    return db.query(Contact).all()
