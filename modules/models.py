from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)   
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="user")  

 
class Service(Base):
    __tablename__ = "services" 


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)


    providers = relationship("Provider", back_populates="service")
    


