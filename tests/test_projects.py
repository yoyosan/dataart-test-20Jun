def test_create_project_user_not_found(client):
    response = client.post(
        "/projects",
        json={
            "name": "Test Project 1",
            "owner_id": "00000000-0000-0000-0000-000000000000",
        },
    )

    assert response.status_code == 404


def test_create_project(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()

    response = client.post(
        "/projects",
        json={
            "name": "Test Project 1",
            "owner_id": user["id"],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project 1"
    assert data["owner_id"] == user["id"]
    assert "id" in data


def test_list_projects(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()
    client.post(
        "/projects",
        json={
            "name": "Test Project 1",
            "owner_id": user["id"],
        },
    )
    client.post(
        "/projects",
        json={
            "name": "Test Project 2",
            "owner_id": user["id"],
        },
    )

    response = client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_projects_pagination(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()
    for i in range(5):
        client.post(
            "/projects",
            json={
                "name": f"Test Project {i}",
                "owner_id": user["id"],
            },
        )

    response = client.get("/projects?limit=2&offset=0")
    assert len(response.json()) == 2


def test_list_projects_pagination_and_offset(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()
    for i in range(5):
        client.post(
            "/projects",
            json={
                "name": f"Test Project {i}",
                "owner_id": user["id"],
            },
        )

    response = client.get("/projects/?limit=10&offset=4")
    assert len(response.json()) == 1


def test_get_project_not_found(client):
    response = client.get("/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_project(client):
    user = client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    ).json()
    project = client.post(
        "/projects",
        json={
            "name": "Test Project 1",
            "owner_id": user["id"],
        },
    ).json()

    response = client.get(f"/projects/{project['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project 1"
