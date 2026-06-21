import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_db
from app.models import Project, User
from app.schemas import ProjectRead, UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])
DBDep = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/",
    response_model=UserRead,
    status_code=201,
    summary="Create a new user",
    description="Create a new user with email validation. Returns 409 if email already exists.",
    responses={409: {"description": "Email already registered"}},
)
async def create_user(user: UserCreate, db: DBDep) -> User:
    db_user = User.model_validate(user)
    db.add(db_user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    await db.refresh(db_user)
    return db_user


@router.get(
    "/",
    response_model=list[UserRead],
    summary="List all users",
    description="Retrieve a paginated list of users.",
)
async def list_users(
    db: DBDep,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[User]:
    return list(
        (await db.execute(select(User).offset(offset).limit(limit))).scalars().all()
    )


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get user by ID",
    responses={404: {"description": "User not found"}},
)
async def get_user(user_id: uuid.UUID, db: DBDep) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get(
    "/{user_id}/projects",
    response_model=list[ProjectRead],
    summary="List user's projects",
    description="Retrieve all projects owned by a specific user.",
    responses={404: {"description": "User not found"}},
)
async def list_user_projects(user_id: uuid.UUID, db: DBDep) -> list[Project]:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return list(
        (await db.execute(select(Project).where(Project.owner_id == user_id)))
        .scalars()
        .all()
    )


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Delete a user",
    description="Delete a user by ID. Returns 409 if user has existing projects.",
    responses={
        404: {"description": "User not found"},
        409: {"description": "Cannot delete user with existing projects"},
    },
)
async def delete_user(user_id: uuid.UUID, db: DBDep) -> None:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(select(Project).where(Project.owner_id == user_id))
    projects = result.scalars().all()
    if projects:
        raise HTTPException(
            status_code=409, detail="Cannot delete user with existing projects"
        )

    await db.delete(user)
    await db.commit()
