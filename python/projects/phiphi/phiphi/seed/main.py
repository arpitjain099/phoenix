"""Main for phiphi seed.

This module is used to seed the database with initial data.

Usage (from the projects/phiphi/):
    python phiphi/seed/main.py
"""
import argparse
import logging

from sqlalchemy.orm import Session

from phiphi import platform_db, utils
from phiphi.seed import (
    apify_facebook_comments,
    apify_facebook_post_gather,
    environments,
    job_runs,
    projects,
    users,
)

utils.init_logging()
utils.init_sentry()

main_logger = logging.getLogger(__name__)


def main(session: Session, testing: bool = False) -> None:
    """Seed the database.

    If testing is true the databased will be dropped and recreated.
    """
    if testing:
        platform_db.Base.metadata.drop_all(
            bind=session.get_bind()
        )  # Drop all tables if --testing flag is provided
        platform_db.Base.metadata.create_all(session.get_bind())  # Create all tables again
    users.init_first_admin_user(session)
    environments.init_main_environment(session)

    if testing:
        users.seed_test_users(session)
        environments.seed_test_environment(session)
        projects.seed_test_project(session)
        apify_facebook_post_gather.seed_test_apify_facebook_post_gathers(session)
        apify_facebook_comments.seed_test_apify_facebook_comment_gathers(session)
        job_runs.seed_test_job_runs(session)


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
