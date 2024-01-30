from sqlalchemy.orm import Session

from models.contacts import User


async def create_user(body: User, db: Session):
    """
    A method for creating new user in database.

    :param body: User
    :param db: Session
    :return: User
    """

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_email(email: str, db: Session):
    """
    A method for getting user by email from database.

    :param email: str
    :param db: Session
    :return: User
    """
    return db.query(User).filter(User.email == email).first()


async def update_token(user: User, token: str | None, db: Session):
    """
    A method for updating user token in database.

    :param user: User
    :param token: str | None
    :param db: Session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session):
    """
    A method for confirming user email.

    :param email: str
    :param db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def set_userpic(userpic: str, db: Session, user: User):
    """
    A method for setting userpic.
    :param userpic: str
    :param db: Session
    :param user: User
    :return: None
    """
    user.userpic = userpic
    db.commit()
