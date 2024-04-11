"""Main for phiphi seed.

This module is used to seed the database with initial data.

Usage (from the projects/phiphi/):
    python phiphi/seed/main.py
"""
import logging

from sqlalchemy.orm import Session

from phiphi import platform_db
from phiphi.seed import environments, gathers, instances, users

main_logger = logging.getLogger("phiphi.seed.main::" + __name__)
main_logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
main_logger.addHandler(ch)


def main(session: Session, testing: bool = False) -> None:
    """Seed the database."""
    users.init_first_admin_user(session)
    if testing:
        users.seed_test_users(session)
        instances.seed_test_instance(session)
        gathers.seed_test_apify_gathers(session)
        environments.seed_test_environment(session)


if __name__ == "__main__":
    main_logger.info("Seeding the database")
    with Session(platform_db.engine) as session:
        main(session)
    main_logger.info("Finished seeding the database")
