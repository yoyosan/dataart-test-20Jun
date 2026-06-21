from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import projects, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title="Mini User & Project Management API",
    description="A small REST API for managing Users and Projects",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(projects.router)
