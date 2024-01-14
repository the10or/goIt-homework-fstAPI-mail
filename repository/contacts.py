from sqlalchemy import func, and_, extract

from models.contacts import ContactDB


class ContactRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self, limit, offset):
        return (
            self.db.query(ContactDB)
            .order_by(ContactDB.id)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_by_id(self, id):
        return self.db.get(ContactDB, id)

    def create(self, contact):
        new_contact = ContactDB(**contact.dict())
        self.db.add(new_contact)
        self.db.commit()
        self.db.refresh(new_contact)
        return new_contact

    def update(self, id, contact):
        existing_contact = self.db.query(ContactDB).filter(ContactDB.id == id).first()

        if existing_contact:
            for field, value in contact.dict().items():
                if value is not None:
                    setattr(existing_contact, field, value)

            self.db.commit()

        return existing_contact

    def get_by_name(self, name):
        return self.db.query(ContactDB).filter(ContactDB.firstname == name).all()

    def get_by_email(self, email):
        return self.db.query(ContactDB).filter(ContactDB.email == email).first()

    def get_by_lastname(self, lastname):
        return self.db.query(ContactDB).filter(ContactDB.lastname == lastname).all()

    def get_by_birthdate(self, today, next_week, year_to_change):
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
                )
            )
            .all()
        )

        return contacts

    def delete(self, id):
        self.db.query(ContactDB).filter(ContactDB.id == id).delete()
        self.db.commit()
        return self.get_by_id(id)
