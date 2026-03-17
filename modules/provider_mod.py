from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

  
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    specialization = Column(String, nullable=False)
    password = Column(String, nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"))

    appointments = relationship("Appointment", back_populates="provider")
    service = relationship("Service", back_populates="providers")
