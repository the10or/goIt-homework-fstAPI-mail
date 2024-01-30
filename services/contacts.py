from datetime import date, timedelta

from models.contacts import User
from repository.contacts import ContactRepository


class ContactService:
    """
    A class for working with contacts.

   """

    def __init__(self, db):
        self.repository = ContactRepository(db)
        self.db = db

    def get_all_contacts(self, limit, offset, user: User):
        """
        A method for getting all contacts for current user.

        :param limit: (int) quantity of contacts on one page
        :param offset: (int) number of skipped contacts
        :param user: (User) current user
        :return:  (list) list of contacts
        """
        return self.repository.get_all(limit, offset, user)

    def get_by_id(self, id: int, user: User):
        """
        A method for getting contact by id.

        :param id: (int) unique contact id
        :param user: (User) current user
        :return: User | None
        """
        return self.repository.get_by_id(id, user)

    def create(self, contact, user: User):
        """
        A method for creating new contact.

        :param contact: (ContactDB) new contact
        :param user:  (User) current user
        :return:   ContactDB

        """
        return self.repository.create(contact, user)

    def update(self, id, contact, user: User):
        """
        A method for updating contact.

        :param id: (int) unique contact id
        :param contact: (ContactDB) new contact
        :param user: (User) current user
        :return: ContactDB | None
        """
        return self.repository.update(id, contact, user)

    def delete(self, id, user: User):
        """
        A method for deleting contact.

        :param id: (int) unique contact id
        :param user: (User) current user
        :return: (ContactDB) deleted contact
        """
        return self.repository.delete(id, user)

    def get_by_name(self, name, user: User):
        """
        A method for getting contact by name.

        :param name: (str) contact name
        :param user: (User) current user
        :return: (ContactDB) contact
        """
        return self.repository.get_by_name(name, user)

    def get_by_email(self, email, user: User):
        """
        A method for getting contact by email.

        :param email: (str) contact email
        :param user: (User) current user
        :return: (ContactDB) contact
        """
        return self.repository.get_by_email(email, user)

    def get_by_lastname(self, lastname, user: User):
        """
        A method for getting contact by lastname.

        :param lastname: (str) contact lastname
        :param user: (User) current user
        :return: (ContactDB) contact
        """
        return self.repository.get_by_lastname(lastname, user)

    def get_by_birthdate(self, user: User):
        """
        A method for getting contact by birthdate.

        :param user: (User) current user
        :return: (ContactDB) contact
        """
        today = date.today()
        next_week = today + timedelta(days=7)
        year_to_change = next_week.year if next_week.year > today.year else today.year
        return self.repository.get_by_birthdate(today, next_week, year_to_change, user)
