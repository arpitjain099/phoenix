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
    apify_facebook_comments_gather,
    apify_facebook_posts_gather,
    apify_tiktok_accounts_posts_gather,
    apify_tiktok_hashtags_posts_gather,
    job_runs,
    projects,
    users,
    workspaces,
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
    workspaces.init_main_workspace(session)

    if testing:
        users.seed_test_users(session)
        workspaces.seed_test_workspace(session)
        projects.seed_test_project(session)
        apify_facebook_posts_gather.seed_test_apify_facebook_posts_gathers(session)
        apify_facebook_comments_gather.seed_test_apify_facebook_comments_gathers(session)
        apify_tiktok_accounts_posts_gather.seed_test_apify_tiktok_accounts_posts_gathers(session)
        apify_tiktok_hashtags_posts_gather.seed_test_apify_tiktok_hashtags_posts_gathers(session)
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
