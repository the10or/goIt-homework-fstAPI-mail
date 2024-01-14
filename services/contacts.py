from datetime import date, timedelta

from repository.contacts import ContactRepository


class ContactService:
    def __init__(self, db):
        self.repository = ContactRepository(db)
        self.db = db

    def get_all_contacts(self, limit, offset):
        return self.repository.get_all(limit, offset)

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, contact):
        return self.repository.create(contact)

    def update(self, id, contact):
        return self.repository.update(id, contact)

    def delete(self, id):
        return self.repository.delete(id)

    def get_by_name(self, name):
        return self.repository.get_by_name(name)

    def get_by_email(self, email):
        return self.repository.get_by_email(email)

    def get_by_lastname(self, lastname):
        return self.repository.get_by_lastname(lastname)

    def get_by_birthdate(self):
        today = date.today()
        next_week = today + timedelta(days=7)
        year_to_change = next_week.year if next_week.year > today.year else today.year
        return self.repository.get_by_birthdate(today, next_week, year_to_change)
