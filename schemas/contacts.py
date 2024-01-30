from datetime import date

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactBase(BaseModel):
    """
    Pydantic schema for contacts table

    :param firstname: (str) first name
    :param lastname: (str) last name
    :param email: (EmailStr) email
    :param phone: (PhoneNumber) phone number
    :param birthdate: (date)  birthdate

    """

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
    """
    Pydantic schema for updating contacts table

    firstname: (str)  first name
    lastname: (str)  last name
    email: (EmailStr)  email
    phone: (PhoneNumber)  phone number
    birthdate: (str)  birthdate

    """
    firstname: str = None
    lastname: str = None
    email: str = None
    phone: str = None
    birthdate: str = None


class ContactResponse(ContactBase):
    """
    Pydantic schema for contacts table response

    :param id: (int) primary key
    """
    id: int

    class Config:
        from_attributes = True
