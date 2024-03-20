"""Seed the users."""
from sqlalchemy.orm import Session

from phiphi.users import crud, schemas


def seed_test_users(session: Session) -> None:
    """Seed the users."""
    users = [
        schemas.UserCreate(email="test1@phiphi.com", display_name="Test User 1"),
        schemas.UserCreate(email="test2@phiphi.com", display_name="Test User 2"),
    ]
    for user in users:
        crud.create_user(session=session, user=user)
