from unittest.mock import MagicMock

from models.contacts import User


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("api.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user["email"]
    assert "id" in data["user"]
    assert mock_send_email.called


def test_create_user_existing_email(client, user, session_with_existing_user):
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "User with this email already exist"


def test_login_user(client, session_with_existing_user, user):
    current_user: User = session_with_existing_user.query(User).first()
    current_user.confirmed = True

    session_with_existing_user.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": "test_password"},
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_email(client, user):
    response = client.post("/api/auth/login", data={"username": "wrongemail", "password": user["password"]})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"
    assert "access_token" not in data
    assert "refresh_token" not in data


def test_login_wrong_password(client, user):
    response = client.post("/api/auth/login",
                                        data={"username": user["email"], "password": "wrongpassword"})

    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"
    assert "access_token" not in data
    assert "refresh_token" not in data
