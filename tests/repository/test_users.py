import unittest
from unittest.mock import Mock, MagicMock, AsyncMock

from sqlalchemy.orm import Session

from repository.users import User, create_user, get_user_by_email, update_token, confirmed_email, set_userpic


class TestUserRepository(unittest.TestCase):

    async def test_create_user_success(self):
        body = User(email="test@example.com", password="securepassword")
        db = Mock(spec=Session)
        new_user = await create_user(body, db)
        self.assertEqual(new_user.email, "test@example.com")
        self.assertEqual(new_user.password, "securepassword")

    async def test_get_user_by_email_returns_user(self):
        email = "test@example.com"
        db_mock = MagicMock()
        user_mock = MagicMock()
        db_mock.query().filter().first.return_value = user_mock

        result = await get_user_by_email(email, db_mock)

        self.assertEqual(result, user_mock)

    async def test_get_user_by_email_handles_no_user_found(self):
        email = "nonexistent@example.com"
        db_mock = MagicMock()
        db_mock.query().filter().first.return_value = None

        result = await get_user_by_email(email, db_mock)
        self.assertIsNone(result)

    async def test_update_token_with_valid_token(self):
        user = MagicMock()
        token = "valid_token"
        db = MagicMock()

        await update_token(user, token, db)
        self.assertEqual(user.refresh_token, "valid_token")

    async def test_update_token_with_none_token(self):
        user = MagicMock()
        token = None
        db = MagicMock()

        await update_token(user, token, db)
        self.assertEqual(user.refresh_token, None)

    async def test_confirmed_email(self):
        user = User(confirmed=False)
        get_user_by_email = AsyncMock(return_value=user)
        db = MagicMock()

        await confirmed_email("test@example.com", db)

        assert user.confirmed

        user = User(confirmed=True)
        get_user_by_email = AsyncMock(return_value=user)
        db = MagicMock()

        await confirmed_email("test@example.com", db)
        assert user.confirmed

        get_user_by_email = AsyncMock(return_value=None)
        db = MagicMock()
        await confirmed_email("nonexistent@example.com", db)

    async def test_set_userpic(self):
        user = MagicMock()
        db = MagicMock()
        userpic = "test_userpic.jpg"
        await set_userpic(userpic, db, user)
        db.commit.assert_called_once()
        self.assertEqual(user.userpic, userpic)


if __name__ == '__main__':
    unittest.main()
