from fastapi import FastAPI

from api.contacts_router import router as contacts_router
from api.auth import router as auth_router
from dependencies.database import engine
from models import contacts

contacts.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/api", tags=["auth"])


@app.get("/")
def health_check():
    return {"status": "ok"}
