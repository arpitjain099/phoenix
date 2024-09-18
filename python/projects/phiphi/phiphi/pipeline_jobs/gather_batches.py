"""Gather batches."""
import pandera as pa

from phiphi.api.projects.gathers import schemas
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils

# TODO: should add BQ cluster specification on columns: gather_id, job_run_id, gather_batch_id
# Schema for gather batches
gather_batches_schema = pa.DataFrameSchema(
    {
        "gather_id": pa.Column(pa.Int, nullable=False),
        "job_run_id": pa.Column(pa.Int, nullable=False),
        "gather_type": pa.Column(
            pa.String,
            checks=pa.Check.isin([e.value for e in schemas.ChildTypeName]),
            nullable=False,
        ),
        "platform": pa.Column(
            pa.String,
            checks=pa.Check.isin([e.value for e in schemas.Platform]),
            nullable=False,
        ),
        "data_type": pa.Column(
            pa.String, checks=pa.Check.isin([e.value for e in schemas.DataType]), nullable=False
        ),
        "batch_id": pa.Column(pa.Int, nullable=False),
        "gathered_at": pipeline_jobs_utils.utc_datetime_column(nullable=False),
        "json_data": pa.Column(pa.String, nullable=False),
        "last_processed_at": pipeline_jobs_utils.utc_datetime_column(nullable=True),
    }
)
