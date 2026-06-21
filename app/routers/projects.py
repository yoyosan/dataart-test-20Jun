import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_db
from app.models import Project, User
from app.schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])
DBDep = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=201,
    summary="Create a new project",
    description="Create a new project for an existing user. Returns 404 if user not found.",
    responses={404: {"description": "User not found"}},
)
async def create_project(project: ProjectCreate, db: DBDep) -> Project:
    owner_exists = await db.get(User, project.owner_id)
    if not owner_exists:
        raise HTTPException(status_code=404, detail="User not found")

    db_project = Project.model_validate(project)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


@router.get(
    "/",
    response_model=list[ProjectRead],
    summary="List all projects",
    description="Retrieve a paginated list of projects.",
)
async def list_projects(
    db: DBDep,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[Project]:
    return list(
        (await db.execute(select(Project).offset(offset).limit(limit))).scalars().all()
    )


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get project by ID",
    responses={404: {"description": "Project not found"}},
)
async def get_project(project_id: uuid.UUID, db: DBDep) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project
