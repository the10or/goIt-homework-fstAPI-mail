from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class ContactDB(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(25))
    lastname = Column(String(25))
    email = Column(String(50), unique=True)
    phone = Column(String)
    birthdate = Column(Date)
