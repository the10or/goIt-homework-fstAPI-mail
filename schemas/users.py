from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """
    Pydantic schema for users table

    :param email: (EmailStr) email
    :param password: (string) password
    :param userpic: (string) user picture

    """

    email: EmailStr
    password: str = Field(min_length=8)
    userpic: str | None = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Pydantic schema for users table response

    :param id: (integer) primary key
    :param email: (EmailStr) email
    """
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    """
    Pydantic schema for JWT access and refresh token

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Pydantic schema for request email

    :param email: (EmailStr) email

    """
    email: EmailStr
