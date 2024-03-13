"""Schemas for the users."""
import datetime

import pydantic


class UserBase(pydantic.BaseModel):
    """User base schema.

    Shared properties of all users.
    """

    email: pydantic.EmailStr | None = None
    display_name: str | None = None


class UserCreate(UserBase):
    """User create schema.

    Properties to receive via API on creation.
    """

    email: pydantic.EmailStr
    display_name: str


class User(UserBase):
    """User schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
