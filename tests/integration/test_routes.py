def test_signup(client):
    response = client.post("/api/auth/signup", json={"username": "Alex", "email": "alex@example.com", "password": "12345678"})
    assert response.status_code == 201


def test_signup_duplicate(client):
    payload = {"username": "Alex", "email": "alex@example.com", "password": "12345678"}
    client.post("/api/auth/signup", json=payload)
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 409


def test_login(client, user):
    response = client.post("/api/auth/login", data={"username": "test@example.com", "password": "12345678"})
    assert response.status_code == 200


def test_me(client, token):
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_create_contact(client, token):
    response = client.post("/api/contacts/", headers={"Authorization": f"Bearer {token}"}, json={"first_name": "Ivan", "last_name": "Petrenko", "email": "ivan@example.com", "phone": "+380501112233", "birthday": "1995-06-03"})
    assert response.status_code == 201
