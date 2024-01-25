from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
