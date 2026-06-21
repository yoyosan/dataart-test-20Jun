def test_create_user_duplicate_email(client):
    client.post("/users", json={"email": "test@example.com", "full_name": "Test User"})
    response = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )

    assert response.status_code == 409


def test_create_user(client):
    response = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_list_users(client):
    client.post("/users", json={"email": "a@test.com"})
    client.post("/users", json={"email": "b@test.com"})

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_users_pagination(client):
    for i in range(5):
        client.post("/users", json={"email": f"u{i}@test.com"})

    response = client.get("/users?limit=2&offset=0")
    assert len(response.json()) == 2


def test_list_users_pagination_and_offset(client):
    for i in range(5):
        client.post("/users", json={"email": f"u{i}@test.com"})

    response = client.get("/users/?limit=10&offset=4")
    assert len(response.json()) == 1


def test_get_user_not_found(client):
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_user(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )
    user_id = user.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_user_projects_not_found(client):
    response = client.get("/users/00000000-0000-0000-0000-000000000000/projects")

    assert response.status_code == 404


def test_get_user_projects(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()
    client.post("/projects", json={"name": "Test Project", "owner_id": user["id"]})
    client.post("/projects", json={"name": "Test Project 2", "owner_id": user["id"]})

    response = client.get(f"/users/{user['id']}/projects")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_user_not_found(client):
    response = client.delete("/users/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_delete_user_has_existing_projects(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()
    client.post("/projects", json={"name": "Test Project", "owner_id": user["id"]})

    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 409


def test_delete_user(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()

    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 204

    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 404
