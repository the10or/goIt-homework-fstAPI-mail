from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ContactDB(Base):
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
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(25), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    userpic = Column(String(255), nullable=True)
