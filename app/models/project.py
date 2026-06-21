import uuid

from sqlmodel import Field, Relationship, SQLModel

from .user import User


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    owner_id: uuid.UUID = Field(foreign_key="user.id")

    owner: User | None = Relationship(back_populates="projects")
