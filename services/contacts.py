from datetime import date, timedelta

from models.contacts import User
from repository.contacts import ContactRepository


class ContactService:
    def __init__(self, db):
        self.repository = ContactRepository(db)
        self.db = db

    def get_all_contacts(self, limit, offset, user: User):
        return self.repository.get_all(limit, offset, user)

    def get_by_id(self, id: int, user: User):
        return self.repository.get_by_id(id, user)

    def create(self, contact):
        return self.repository.create(contact)

    def update(self, id, contact):
        return self.repository.update(id, contact)

    def delete(self, id, user: User):
        return self.repository.delete(id, user)

    def get_by_name(self, name, user: User):
        return self.repository.get_by_name(name, user)

    def get_by_email(self, email, user: User):
        return self.repository.get_by_email(email, user)

    def get_by_lastname(self, lastname, user: User):
        return self.repository.get_by_lastname(lastname, user)

    def get_by_birthdate(self, user: User):
        today = date.today()
        next_week = today + timedelta(days=7)
        year_to_change = next_week.year if next_week.year > today.year else today.year
        return self.repository.get_by_birthdate(today, next_week, year_to_change, user)
