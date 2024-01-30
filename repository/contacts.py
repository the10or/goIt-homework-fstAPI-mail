from sqlalchemy import func, and_, extract

from models.contacts import ContactDB, User


class ContactRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self, limit: int, offset: int, user: User):

        """
        A method for getting all contacts for current user.


        :param limit: int
        :param offset: int
        :param user: User
        :return: list
        """

        return (
            self.db.query(ContactDB)
            .filter(ContactDB.user_id == user.id)
            .order_by(ContactDB.id)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_by_id(self, id: int, user: User):
        """
        A method for getting contact by id.
        :param id: int
        :param user: User
        :return: ContactDB
        """
        return self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first()

    def create(self, contact: ContactDB, user: User):
        """
        A method for creating new contact.

        :param contact: ContactDB
        :param user: User
        :return: ContactDB
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

        :param id: int
        :param contact: ContactDB
        :param user: User
        :return: ContactDB
        """
        existing_contact = (self.db.query(ContactDB).
                            filter(and_(ContactDB.id == id,
                                        ContactDB.user_id == user.id))
                            .first())

        if existing_contact:
            for field, value in contact.dict().items():
                if value is not None:
                    setattr(existing_contact, field, value)

            self.db.commit()

        return existing_contact

    def get_by_name(self, name: str, user: User):
        """
        A method for getting contact by name.

        :param name: str
        :param user: User
        :return: ContactDB
        """
        return self.db.query(ContactDB).filter(and_(ContactDB.firstname == name, ContactDB.user_id == user.id)).all()

    def get_by_email(self, email: str, user: User):
        """
        A method for getting contact by email.

        :param email: str
        :param user: User
        :return: ContactDB
        """
        return self.db.query(ContactDB).filter((ContactDB.email == email, ContactDB.user_id == user.id)).first()

    def get_by_lastname(self, lastname, user: User):
        """
        A method for getting contact by lastname.

        :param lastname: str
        :param user: User
        :return: ContactDB
        """
        return self.db.query(ContactDB).filter(and_(ContactDB.lastname == lastname, ContactDB.user_id == user.id)).all()

    def get_by_birthdate(self, today: str, next_week: str, year_to_change: str, user: User):

        """
        A method for getting contacts by birthdate.

        :param today:
        :param next_week:
        :param year_to_change:
        :param user:
        :return:
        """
        contacts = (
            self.db.query(ContactDB)
            .filter(
                and_(
                    func.date(
                        func.concat(
                            year_to_change,
                            "-",
                            extract("month", ContactDB.birthdate),
                            "-",
                            extract("day", ContactDB.birthdate),
                        )
                    )
                    >= today,
                    func.date(
                        func.concat(
                            year_to_change,
                            "-",
                            extract("month", ContactDB.birthdate),
                            "-",
                            extract("day", ContactDB.birthdate),
                        )
                    )
                    <= next_week,
                    ContactDB.user_id == user.id,
                )
            )
            .all()
        )

        return contacts

    def delete(self, id, user: User):
        """
        A method for deleting contact.

        :param id:
        :param user:
        :return:
        """
        contact = self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first()
        if contact:
            self.db.delete(contact)
        self.db.commit()
        return contact
