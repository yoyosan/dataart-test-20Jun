# Mini User & Project Management API

A small REST API built with FastAPI, Pydantic, and SQLModel for managing Users and Projects.

## Quick Start

```bash
docker-compose up --build
```

API available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Validation | Pydantic |
| ORM | SQLModel / SQLAlchemy |
| Database | PostgreSQL 16 |
| Container | Docker + Docker Compose |

## Project Structure

```
app/
├── config.py              # Pydantic BaseSettings (env vars)
├── database.py            # Engine, session factory, dependency injection
├── main.py                # FastAPI app, lifespan, router registration
├── models/
│   ├── user.py            # User table (SQLModel)
│   └── project.py         # Project table (SQLModel)
├── schemas/
│   ├── user.py            # UserCreate, UserRead (Pydantic)
│   └── project.py         # ProjectCreate, ProjectRead (Pydantic)
└── routers/
    ├── users.py           # /users endpoints
    └── projects.py        # /projects endpoints
```

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users` | Create a user (validates email uniqueness) |
| `GET` | `/users` | List users (pagination: `limit`, `offset`) |
| `GET` | `/users/{id}` | Get user by ID |
| `DELETE` | `/users/{id}` | Delete user (rejects if user has projects) |
| `GET` | `/users/{id}/projects` | List projects owned by user |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/projects` | Create a project (validates owner exists) |
| `GET` | `/projects` | List projects (pagination: `limit`, `offset`) |
| `GET` | `/projects/{id}` | Get project by ID |

## Example Usage

```bash
# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "full_name": "John Doe"}'

# List users
curl http://localhost:8000/users?limit=10&offset=0

# Create a project
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "owner_id": "<user-uuid>"}'

# List user's projects
curl http://localhost:8000/users/<user-uuid>/projects
```

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

## Configuration

Environment variables (set in `.env` or `docker-compose.yml`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |

## Design Decisions

- **Dependency Injection**: Database sessions injected via FastAPI's `Depends`
- **Separation of Concerns**: Models (DB), Schemas (API), Routers (endpoints)
- **Delete Protection**: Users with projects cannot be deleted (returns 409)
- **UUID Primary Keys**: Distributed-friendly, no sequential ID leaks
- **Typed Config**: Pydantic BaseSettings validates configuration at startup
