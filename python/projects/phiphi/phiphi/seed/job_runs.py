"""Seed the Job runs.

We are using a very simple and brittle seeding of the database.

In that we have to check the ids of the projects and gathers in the database
to seed the correct job runs.

Currently this script will seed 3 job runs in the database. This includes a job run for all the
apify_facebook_gathers:
- 2 job runs in project 1
- 1 job run in project 2
"""
from sqlalchemy.orm import Session

from phiphi.api.projects.job_runs import crud, schemas

TEST_JOB_RUN = schemas.JobRunCreate(foreign_id=1, foreign_job_type=schemas.ForeignJobType.gather)

TEST_JOB_RUN_2 = schemas.JobRunCreate(foreign_id=2, foreign_job_type=schemas.ForeignJobType.gather)

TEST_JOB_RUN_3 = schemas.JobRunCreate(foreign_id=3, foreign_job_type=schemas.ForeignJobType.gather)


def seed_test_job_runs(session: Session) -> None:
    """Seed the job runs."""
    job_runs_project_1 = [TEST_JOB_RUN, TEST_JOB_RUN_2]

    for job_run in job_runs_project_1:
        crud.create_job_run(db=session, project_id=1, job_run_create=job_run)

    crud.create_job_run(db=session, project_id=2, job_run_create=TEST_JOB_RUN_3)
