import pytest


@pytest.mark.asyncio
async def test_create_project_user_not_found(client):
    response = await client.post(
        "/projects",
        json={
            "name": "Test Project 1",
            "owner_id": "00000000-0000-0000-0000-000000000000",
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_project(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()

    response = await client.post(
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


@pytest.mark.asyncio
async def test_list_projects(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()
    await client.post(
        "/projects",
        json={
            "name": "Test Project 1",
            "owner_id": user["id"],
        },
    )
    await client.post(
        "/projects",
        json={
            "name": "Test Project 2",
            "owner_id": user["id"],
        },
    )

    response = await client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_projects_pagination(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()
    for i in range(5):
        await client.post(
            "/projects",
            json={
                "name": f"Test Project {i}",
                "owner_id": user["id"],
            },
        )

    response = await client.get("/projects?limit=2&offset=0")
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_projects_pagination_and_offset(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()
    for i in range(5):
        await client.post(
            "/projects",
            json={
                "name": f"Test Project {i}",
                "owner_id": user["id"],
            },
        )

    response = await client.get("/projects/?limit=10&offset=4")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_project_not_found(client):
    response = await client.get("/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_project(client):
    user = (
        await client.post(
            "/users", json={"email": "test@example.com", "full_name": "Test User"}
        )
    ).json()
    project = (
        await client.post(
            "/projects",
            json={
                "name": "Test Project 1",
                "owner_id": user["id"],
            },
        )
    ).json()

    response = await client.get(f"/projects/{project['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project 1"
