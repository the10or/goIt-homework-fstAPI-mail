from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ContactDB(Base):
    """
    SQLAlchemy model for contacts table
    inherits from Base class from sqlalchemy

    Has one-to-many relationship with User

    :param id: (integer) primary key
    :param firstname: (string) first name
    :param lastname: (string) last name
    :param email: (string) email
    :param phone: (string) phone number
    :param birthdate: (date)  birthdate
    :param user_id: (integer) foreign key to users table
    :param user: one-to-many relationship with User

    """

    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(25))
    lastname = Column(String(25))
    email = Column(String(50), unique=True)
    phone = Column(String)
    birthdate = Column(Date)
    user_id = Column('user_id',
                     ForeignKey('users.id', ondelete='CASCADE'),
                     default=None)
    user = relationship('User', backref='contacts')


class User(Base):
    """
    SQLAlchemy model for users table
    inherits from Base class from sqlalchemy

    Has one-to-many relationship with ContactDB

    :param id: (integer) primary key
    :param email: (string) email
    :param password: (string) password
    :param refresh_token: (string) refresh token
    :param confirmed: (boolean) user confirmed or not
    :param userpic: (string) user picture
    :param contacts: one-to-many relationship with ContactDB

    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(25), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    userpic = Column(String(255), nullable=True)
