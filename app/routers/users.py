import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_db
from app.models import Project, User
from app.schemas import ProjectRead, UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])
DBDep = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: DBDep) -> User:
    email_exists = db.exec(select(User).where(User.email == user.email)).first()
    if email_exists:
        raise HTTPException(status_code=409, detail="Email already registered")

    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserRead])
def list_users(
    db: DBDep,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[User]:
    return list(db.exec(select(User).offset(offset).limit(limit)).all())


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, db: DBDep) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{user_id}/projects", response_model=list[ProjectRead])
def list_user_projects(user_id: uuid.UUID, db: DBDep) -> list[Project]:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return list(db.exec(select(Project).where(Project.owner_id == user_id)).all())


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: DBDep) -> None:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.projects:
        raise HTTPException(
            status_code=409, detail="Cannot delete user with existing projects"
        )

    db.delete(user)
    db.commit()
