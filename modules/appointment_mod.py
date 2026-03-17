from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    additional = Column(String, nullable=True)

    service_id = Column(Integer, ForeignKey("services.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="Pending")

    # Relationships
    service = relationship("Service")
    provider = relationship("Provider")
    user = relationship("User")


