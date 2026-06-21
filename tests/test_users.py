import pytest


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    await client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )
    response = await client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_users(client):
    await client.post("/users", json={"email": "a@test.com"})
    await client.post("/users", json={"email": "b@test.com"})

    response = await client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_users_pagination(client):
    for i in range(5):
        await client.post("/users", json={"email": f"u{i}@test.com"})

    response = await client.get("/users?limit=2&offset=0")
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_users_pagination_and_offset(client):
    for i in range(5):
        await client.post("/users", json={"email": f"u{i}@test.com"})

    response = await client.get("/users/?limit=10&offset=4")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user(client):
    user = await client.post(
        "/users", json={"email": "test@example.com", "full_name": "Test User"}
    )
    user_id = user.json()["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_projects_not_found(client):
    response = await client.get("/users/00000000-0000-0000-0000-000000000000/projects")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_projects(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()
    await client.post(
        "/projects", json={"name": "Test Project", "owner_id": user["id"]}
    )
    await client.post(
        "/projects", json={"name": "Test Project 2", "owner_id": user["id"]}
    )

    response = await client.get(f"/users/{user['id']}/projects")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    response = await client.delete("/users/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_has_existing_projects(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()
    await client.post(
        "/projects", json={"name": "Test Project", "owner_id": user["id"]}
    )

    response = await client.delete(f"/users/{user['id']}")
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_delete_user(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()

    response = await client.delete(f"/users/{user['id']}")
    assert response.status_code == 204

    response = await client.get(f"/users/{user['id']}")
    assert response.status_code == 404
