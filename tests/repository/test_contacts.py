import unittest
from unittest.mock import Mock

from models.contacts import ContactDB, User
from repository.contacts import ContactRepository


class TestContactRepository(unittest.TestCase):
    def setUp(self):
        self.db_mock = Mock()
        self.user = User(id=1)
        self.contact_repo = ContactRepository(self.db_mock)

    def test_get_all_returns_list_of_contacts(self):
        expected_contacts = [ContactDB(id=1, user_id=1, firstname="John"),
                             ContactDB(id=2, user_id=1, firstname="Alice")]
        (self.db_mock.query.return_value.filter.return_value.order_by.return_value.
         limit.return_value.offset.return_value.all).return_value = expected_contacts

        actual_contacts = self.contact_repo.get_all(limit=10, offset=0, user=self.user)

        self.assertEqual(actual_contacts, expected_contacts)

    def test_get_by_id_returns_contact(self):
        expected_contact = ContactDB(id=1, user_id=1, firstname="John")
        self.db_mock.query.return_value.filter.return_value.first.return_value = expected_contact

        actual_contact = self.contact_repo.get_by_id(id=1, user=self.user)

        self.assertEqual(actual_contact, expected_contact)

    def test_get_by_name_returns_list_of_contacts(self):
        expected_contacts = [ContactDB(id=1, user_id=1, firstname="John"),
                             ContactDB(id=2, user_id=1, firstname="Alice")]
        self.db_mock.query.return_value.filter.return_value.all.return_value = expected_contacts

        actual_contacts = self.contact_repo.get_by_name(name="John", user=self.user)

        self.assertEqual(actual_contacts, expected_contacts)

    def test_get_by_lastname_returns_list_of_contacts(self):
        expected_contacts = [
            ContactDB(id=1, user_id=1, lastname="Johnson"),
            ContactDB(id=2, user_id=1, lastname="Alison")
        ]
        self.db_mock.query.return_value.filter.return_value.all.return_value = expected_contacts

        actual_contacts = self.contact_repo.get_by_lastname(lastname="Johnson", user=self.user)

        self.assertEqual(actual_contacts, expected_contacts)

    def test_get_by_email_returns_contact(self):
        expected_contact = ContactDB(id=1, user_id=1, email="bNQwv@example.com")

        self.db_mock.query.return_value.filter.return_value.first.return_value = expected_contact

    def test_get_by_email_returns_none(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None


if __name__ == "__main__":
    unittest.main()
