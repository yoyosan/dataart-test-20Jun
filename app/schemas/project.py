import uuid

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field


class ProjectCreate(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    owner_id: uuid.UUID


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
