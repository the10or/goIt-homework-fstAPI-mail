from datetime import date

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr = Field(default="")
    phone: PhoneNumber = Field(default="")
    birthdate: date = Field(default=None)

    class Config:
        validate_assignment = True


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    firstname: str = None
    lastname: str = None
    email: str = None
    phone: str = None
    birthdate: str = None


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
