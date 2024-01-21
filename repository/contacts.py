from sqlalchemy import func, and_, extract

from models.contacts import ContactDB, User


class ContactRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self, limit, offset, user: User):
        return (
            self.db.query(ContactDB)
            .filter(ContactDB.user_id == user.id)
            .order_by(ContactDB.id)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_by_id(self, id, user: User):
        return self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first()

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

    def get_by_name(self, name, user: User):
        return self.db.query(ContactDB).filter(and_(ContactDB.firstname == name, ContactDB.user_id == user.id)).all()

    def get_by_email(self, email, user: User):
        return self.db.query(ContactDB).filter((ContactDB.email == email, ContactDB.user_id == user.id)).first()

    def get_by_lastname(self, lastname, user: User):
        return self.db.query(ContactDB).filter(and_(ContactDB.lastname == lastname, ContactDB.user_id == user.id)).all()

    def get_by_birthdate(self, today, next_week, year_to_change, user: User):
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
        contact = self.db.query(ContactDB).filter(and_(ContactDB.id == id, ContactDB.user_id == user.id)).first()
        if contact:
            self.db.delete(contact)
        self.db.commit()
        return contact
