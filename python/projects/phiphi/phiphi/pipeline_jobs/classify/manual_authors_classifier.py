"""Manual authors classifier module.

This will be applied to manual_post_authors and other possible manual authors classifiers in the
future.
"""
import pandas as pd
import prefect

from phiphi.api.projects.classifiers.manual_post_authors import schemas
from phiphi.pipeline_jobs import classified_authors, utils


@prefect.task
def classify(
    classifier: schemas.ManualPostAuthorsClassifierPipeline, bigquery_dataset: str, job_run_id: int
) -> None:
    """Classify messages using manual authors classifier through BigQuery query."""
    version = classifier.latest_version
    classified_authors_df = pd.DataFrame(version.params["author_classes"])
    classified_authors_df["classifier_id"] = classifier.id
    classified_authors_df["classifier_version_id"] = version.version_id
    classified_authors_df["job_run_id"] = job_run_id
    classified_authors.classified_authors_schema.validate(classified_authors_df)
    utils.write_data(
        classified_authors_df,
        bigquery_dataset,
        classified_authors.constants.CLASSIFIED_AUTHORS_TABLE_NAME,
    )
