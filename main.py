from fastapi import FastAPI
from router import auth,services,appointment,providers,contact,providers_auth
from db.database import Base,engine
from modules import appointment_mod, provider_mod,contact_mod,models

from fastapi.middleware.cors import CORSMiddleware

 
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(providers_auth.router)
app.include_router(services.router)
app.include_router(appointment.router)
app.include_router(providers.router) 
app.include_router(contact.router)
