from fastapi import APIRouter, Depends, status, Response
from starlette.responses import JSONResponse

from dependencies.database import get_db, SessionLocal
from schemas.contacts import ContactCreate, ContactUpdate, ContactResponse
from services.contacts import ContactService

router = APIRouter()


@router.get("/", response_model=list[ContactResponse], tags=["get"])
def get_all_contacts(
    limit: int = 10, offset: int = 0, db: SessionLocal = Depends(get_db)
):
    return ContactService(db).get_all_contacts(limit=limit, offset=offset)


@router.get("/{id:int}", response_model=ContactResponse, tags=["get"])
def get_contact_by_id(id: int, db: SessionLocal = Depends(get_db)):
    contact = ContactService(db).get_by_id(id)
    if not contact:
        return JSONResponse(
            content={"message": "not found"}, status_code=status.HTTP_204_NO_CONTENT
        )
    return contact


@router.get("/{name:str}", response_model=list[ContactResponse], tags=["get"])
def get_contact_by_name(name: str, db: SessionLocal = Depends(get_db)):
    contact = ContactService(db).get_by_name(name)
    if not contact:
        return JSONResponse(
            content={"message": "not found"}, status_code=status.HTTP_204_NO_CONTENT
        )
    return contact


@router.get("/email/{email:str}", response_model=ContactResponse, tags=["get"])
def get_contact_by_email(email: str, db: SessionLocal = Depends(get_db)):
    contact = ContactService(db).get_by_email(email)
    if not contact:
        return JSONResponse(
            content={"message": "not found"}, status_code=status.HTTP_204_NO_CONTENT
        )
    return contact


@router.get(
    "/lastname/{lastname:str}", response_model=list[ContactResponse], tags=["get"]
)
def get_contact_by_lastname(lastname: str, db: SessionLocal = Depends(get_db)):
    contact = ContactService(db).get_by_lastname(lastname)
    if not contact:
        return JSONResponse(
            content={"message": "not found"}, status_code=status.HTTP_204_NO_CONTENT
        )
    return contact


@router.get("/api/birthdays", response_model=list[ContactResponse], tags=["get"])
def get_by_birthdate(db: SessionLocal = Depends(get_db)):
    contact = ContactService(db).get_by_birthdate()
    if not contact:
        return []
    return contact


@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: SessionLocal = Depends(get_db)):
    contact_service = ContactService(db)
    created_contact = contact_service.create(contact)
    print("+++++++++++")
    print(created_contact)
    print("+++++++++++")
    response_contact = ContactResponse(
        id=created_contact.id,
        firstname=created_contact.firstname,
        lastname=created_contact.lastname,
        email=created_contact.email,
        phone=created_contact.phone,
        birthdate=created_contact.birthdate,
    )
    return response_contact


@router.put("/{id}", response_model=ContactResponse)
def update_contact(id: int, contact: ContactUpdate, db: SessionLocal = Depends(get_db)):
    return ContactService(db).update(id, contact)


@router.delete("/{id}")
def delete_contact(id: int, db: SessionLocal = Depends(get_db)):
    contact = ContactService(db).delete(id)
    return Response(
        content="contact is deleted",
        media_type="text/plain",
        status_code=status.HTTP_204_NO_CONTENT,
    )
