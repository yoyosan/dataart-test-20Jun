# Mini User & Project Management API — Requirements

## Goal

Implement a small REST API using FastAPI, Pydantic, and SQLModel/SQLAlchemy.

- No UI required.
- The application must start locally using `docker-compose up` without any manual steps.
- The application should be able to create Users and assign them to Projects.

---

## Functional Requirements

### Domain Model

| Entity | Fields | Relationship |
|--------|--------|--------------|
| **User** | id, email, name | One User → Many Projects |
| **Project** | id, name, description, owner_id | Many Projects → One User |

### API Endpoints

#### Users

| Method | Endpoint | Description | Notes |
|--------|----------|-------------|-------|
| `POST` | `/users` | Create a user | Validate email uniqueness |
| `GET` | `/users/{id}` | Retrieve user by ID | — |
| `GET` | `/users` | List users | Pagination required: `limit`, `offset` |
| `DELETE` | `/users/{id}` | Delete user by ID | Ensure Projects are updated |

#### Projects

| Method | Endpoint | Description | Notes |
|--------|----------|-------------|-------|
| `POST` | `/projects` | Create a project for existing users | — |
| `GET` | `/projects/{id}` | Retrieve project by ID | — |
| `GET` | `/users/{id}/projects` | List all projects owned by a user | — |

---

## Non-Functional Requirements

### Docker & Local Execution

- The project must run with only: `docker-compose up`
- No extra commands allowed.
- `docker-compose` must:
  - Start API service
  - Start DB service
  - Expose API on `http://localhost:8000`
  - Automatically create DB schema

---

## Evaluation Criteria

### Core (Must-have)

- [x] Correct FastAPI usage
- [x] Clean Pydantic models
- [x] Correct ORM modeling & relationships
- [x] Docker-compose works out of the box
- [x] Code readability and separation of concerns

### Bonus (Optional)

- [x] Dependency injection for DB sessions
- [x] Async SQLAlchemy/SQLModel
- [x] Tests (pytest)
- [x] OpenAPI tags & descriptions

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Validation | Pydantic |
| ORM | SQLModel / SQLAlchemy |
| Database | PostgreSQL |
| Container | Docker + Docker Compose |
