from faker import Faker
from faker.providers.phone_number import Provider

from dependencies.database import SessionLocal
from models.contacts import ContactDB

fake = Faker(locale="en_US")
fake.add_provider(Provider)

session = SessionLocal()


def create_fake_contacts(num_contacts):
    for _ in range(num_contacts):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = fake.email()

        phone = fake.phone_number()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=90)

        contact = ContactDB(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            birthdate=birthdate,
        )
        session.add(contact)

    session.commit()


if __name__ == "__main__":
    num_contacts = 1000
    create_fake_contacts(num_contacts)
    print(f"Successfully created {num_contacts} fake contacts.")
