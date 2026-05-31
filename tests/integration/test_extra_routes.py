from src.entity.models import User
from src.services.auth import create_reset_password_token, get_password_hash


def test_login_wrong_password(client, user):
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401


def test_contacts_without_token(client):
    response = client.get("/api/contacts/")

    assert response.status_code == 401


def test_get_contact_by_id(client, token):
    create_response = client.post(
        "/api/contacts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "email": "ivan1@example.com",
            "phone": "+380501112233",
            "birthday": "1995-06-03",
            "additional_data": "test",
        },
    )

    contact_id = create_response.json()["id"]

    response = client.get(
        f"/api/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == contact_id


def test_update_contact(client, token):
    create_response = client.post(
        "/api/contacts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "email": "ivan2@example.com",
            "phone": "+380501112233",
            "birthday": "1995-06-03",
            "additional_data": "test",
        },
    )

    contact_id = create_response.json()["id"]

    response = client.put(
        f"/api/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "Petro",
            "last_name": "Ivanenko",
            "email": "petro@example.com",
            "phone": "+380671112233",
            "birthday": "1992-07-04",
            "additional_data": "updated",
        },
    )

    assert response.status_code == 200
    assert response.json()["first_name"] == "Petro"


def test_delete_contact(client, token):
    create_response = client.post(
        "/api/contacts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "email": "ivan3@example.com",
            "phone": "+380501112233",
            "birthday": "1995-06-03",
            "additional_data": "test",
        },
    )

    contact_id = create_response.json()["id"]

    response = client.delete(
        f"/api/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_birthdays(client, token):
    response = client.get(
        "/api/contacts/birthdays",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_request_password_reset(client, user):
    response = client.post(
        "/api/auth/request_password_reset",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 200


def test_reset_password(client, db_session, user):
    token = create_reset_password_token("test@example.com")

    response = client.post(
        "/api/auth/reset_password",
        json={
            "token": token,
            "new_password": "87654321",
        },
    )

    assert response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "87654321",
        },
    )

    assert login_response.status_code == 200


def test_avatar_forbidden_for_user(client, token):
    response = client.patch(
        "/api/users/avatar",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("avatar.png", b"fake-image", "image/png")},
    )

    assert response.status_code == 403


def test_unconfirmed_user_login(client, db_session):
    user = User(
        username="No Confirm",
        email="noconfirm@example.com",
        password=get_password_hash("12345678"),
        confirmed=False,
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        data={
            "username": "noconfirm@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 401