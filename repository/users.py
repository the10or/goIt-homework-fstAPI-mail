from sqlalchemy.orm import Session

from models.contacts import User


async def create_user(body: User, db: Session):
    """
    A method for creating new user in database.

    :param body: data of new user
    :param db: database session
    :return: new user
    """

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_email(email: str, db: Session):
    """
    A method for getting user by email from database.

    :param email: user email
    :param db: database session
    :return: found user
    """
    return db.query(User).filter(User.email == email).first()


async def update_token(user: User, token: str | None, db: Session):
    """
    A method for updating user token in database.

    :param user: user owning token
    :param token: token to be updated
    :param db: database session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session):
    """
    A method for confirming user email.

    :param email: email of user that need to be confirmed
    :param db: database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def set_userpic(userpic: str, db: Session, user: User):
    """
    A method for setting userpic.
    :param userpic: address of userpic
    :param db: database session
    :param user: current user
    :return: None
    """
    user.userpic = userpic
    db.commit()
