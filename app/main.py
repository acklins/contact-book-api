from fastapi import FastAPI
from app.routers import contacts

app = FastAPI()

app.include_router(
    contacts.router, 
    prefix="/contacts",
    tags=["contacts"]
)