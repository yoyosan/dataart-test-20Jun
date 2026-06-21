import uuid

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlmodel import Field


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=255)
    full_name: str | None = Field(default=None, max_length=255)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str | None
