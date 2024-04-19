"""Main for phiphi seed.

This module is used to seed the database with initial data.

Usage (from the projects/phiphi/):
    python phiphi/seed/main.py
"""
import argparse
import logging

from sqlalchemy.orm import Session

from phiphi import platform_db
from phiphi.seed import environments, gathers, project_runs, projects, users

main_logger = logging.getLogger("phiphi.seed.main::" + __name__)
main_logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
main_logger.addHandler(ch)


def main(session: Session, testing: bool = False) -> None:
    """Seed the database."""
    if testing:
        #This drops and recreates the main database
        platform_db.Base.metadata.drop_all(
            bind=platform_db.engine
        )  # Drop all tables if --testing flag is provided
        platform_db.Base.metadata.create_all(bind=platform_db.engine)  # Create all tables again
    users.init_first_admin_user(session)
    environments.init_main_environment(session)

    if testing:
        users.seed_test_users(session)
        environments.seed_test_environment(session)
        projects.seed_test_project(session)
        gathers.seed_test_apify_gathers(session)
        project_runs.seed_test_project_runs(session)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database", prog="main")
    parser.add_argument(
        "--testing", action="store_true", help="Drop and recreate the database for testing"
    )
    args = parser.parse_args()

    if args.testing:
        main_logger.info("Seeding the database --testing")
    else:
        main_logger.info("Seeding the database")
    with Session(platform_db.engine) as session:
        main(session, args.testing)
    main_logger.info("Finished seeding the database")
