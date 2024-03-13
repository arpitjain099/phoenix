"""Main for phiphi seed.

This module is used to seed the database with initial data.

Usage (from the projects/phiphi/):
    python phiphi/seed/main.py
"""
import logging

from sqlalchemy.orm import Session

from phiphi.core import config, db
from phiphi.users import crud, schemas

main_logger = logging.getLogger("phiphi.seed.main::" + __name__)
main_logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
main_logger.addHandler(ch)


def init_first_admin_user(session: Session) -> schemas.User:
    """Create the first admin."""
    user = crud.read_user(session, 1)
    if not user:
        user_in = schemas.UserCreate(
            email=config.settings.FIRST_ADMINUSEREMAIL,
            display_name=config.settings.FIRST_ADMINUSERDISPLAYNAME,
        )
        user = crud.create_user(session=session, user=user_in)
    return user


def main(session: Session) -> None:
    """Seed the database."""
    init_first_admin_user(session)


if __name__ == "__main__":
    main_logger.info("Seeding the database")
    with Session(db.engine) as session:
        main(session)
    main_logger.info("Finished seeding the database")
