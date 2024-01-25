from sqlalchemy.orm import Session

from models.contacts import User
from schemas.users import UserBase


async def create_user(body: User, db: Session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


async def update_token(user: User, token: str | None, db):
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session):
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
