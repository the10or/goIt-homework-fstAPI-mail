from sqlalchemy import func, and_, extract

from models.contacts import ContactDB, User


class ContactRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self, limit: int, offset: int, user: User):

        """
        A method for getting all contacts for current user.

        :param limit: number of contacts on one page
        :param offset: number of skipped contacts
        :param user: current user
        :return: list of contacts
        """

        return (
            self.db.query(ContactDB).filter(ContactDB.user_id == user.id).order_by(ContactDB.id).limit(limit).offset(
                offset).all())

    def get_by_id(self, id: int, user: User):
        """
        A method for getting contact by id.
        :param id: id of contact
        :param user: current user
        :return: contact data by id
        """
        return self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first()

    def create(self, contact: ContactDB, user: User):
        """
        A method for creating new contact.

        :param contact: contact data
        :param user: current user
        :return: new contact data
        """
        new_contact = ContactDB(**contact.dict())
        new_contact.user_id = user.id
        self.db.add(new_contact)
        self.db.commit()
        self.db.refresh(new_contact)
        return new_contact

    def update(self, id: int, contact: ContactDB, user: User):
        """
        A method for updating contact.

        :param id: id of contact
        :param contact: contact data
        :param user: current user
        :return: updated contact data
        """
        existing_contact = (
            self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first())

        if existing_contact:
            for field, value in contact.dict().items():
                if value is not None:
                    setattr(existing_contact, field, value)

            self.db.commit()

        return existing_contact

    def get_by_name(self, name: str, user: User):
        """
        A method for getting contact by name.

        :param name: firstname of searched contact
        :param user: current user
        :return: list of found contacts
        """
        return self.db.query(ContactDB).filter(and_(ContactDB.firstname == name, ContactDB.user_id == user.id)).all()

    def get_by_email(self, email: str, user: User):
        """
        A method for getting contact by email.

        :param email: email of searched contact
        :param user: current user
        :return: contact with given email
        """
        return self.db.query(ContactDB).filter((ContactDB.email == email, ContactDB.user_id == user.id)).first()

    def get_by_lastname(self, lastname, user: User):
        """
        A method for getting contact by lastname.

        :param lastname: lastname of searched contact
        :param user: current user
        :return: list of found contacts
        """
        return self.db.query(ContactDB).filter(and_(ContactDB.lastname == lastname, ContactDB.user_id == user.id)).all()

    def get_by_birthdate(self, today: str, next_week: str, year_to_change: str, user: User):

        """
        A method for getting contacts by birthdate.

        :param today: current date
        :param next_week: date of next week
        :param year_to_change: year needed to be changed in birthdate
        :param user: current user
        :return: list of found contacts
        """
        contacts = (self.db.query(ContactDB).filter(and_(func.date(
            func.concat(year_to_change, "-", extract("month", ContactDB.birthdate), "-",
                extract("day", ContactDB.birthdate), )) >= today, func.date(
            func.concat(year_to_change, "-", extract("month", ContactDB.birthdate), "-",
                extract("day", ContactDB.birthdate), )) <= next_week, ContactDB.user_id == user.id, )).all())

        return contacts

    def delete(self, id, user: User):
        """
        A method for deleting contact.

        :param id: id of contact to be deleted
        :param user: current user
        :return: deleted contact
        """
        contact = self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first()
        if contact:
            self.db.delete(contact)
        self.db.commit()
        return contact
