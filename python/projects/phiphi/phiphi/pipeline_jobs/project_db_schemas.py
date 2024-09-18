"""Tables schemas for the project database."""
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


# TODO: should add BQ cluster specification on columns:
#  - platform, data_type, phoenix_platform_message_id, platform_message_last_updated_at
# Even better would be including `phoenix_processed_at` on the end, but BQ limits to 4 cols.
# We could assuming that messages IDs are unique across platforms, but I don't think this is really
# guaranteed.
generalised_messages_schema = pa.DataFrameSchema(
    {
        "gather_id": pa.Column(pa.Int, nullable=False),
        "gather_batch_id": pa.Column(pa.Int, nullable=False),
        "gathered_at": pipeline_jobs_utils.utc_datetime_column(nullable=False),
        "phoenix_processed_at": pipeline_jobs_utils.utc_datetime_column(nullable=False),
        "gather_type": pa.Column(
            pa.String,
            checks=pa.Check.isin([e.value for e in schemas.ChildTypeName]),
            nullable=False,
        ),
        # NOTE: combination of (platform, data_type, pi_platform_message_id) should give a unique
        # message, but it won't be a unique row as we process the same message multiple times.
        # Doing groupby on these columns then getting MAX(phoenix_processed_at) will give the
        # latest set of unique messages. `phoenix_platform_message_id` can be used instead of
        # `pi_platform_message_id` in the groupby also.
        "platform": pa.Column(
            pa.String,
            checks=pa.Check.isin([e.value for e in schemas.Platform]),
            nullable=False,
        ),
        "data_type": pa.Column(
            pa.String, checks=pa.Check.isin([e.value for e in schemas.DataType]), nullable=False
        ),
        "pi_platform_message_id": pa.Column(pa.String, nullable=True),
        "pi_platform_message_author_id": pa.Column(pa.String, nullable=True),
        "pi_platform_message_author_name": pa.Column(pa.String, nullable=True),
        # For comments this is the post that the comment is on OR the comment that the reply is on.
        "pi_platform_parent_message_id": pa.Column(pa.String, nullable=True),
        # For comments this is the root post for that comment. For posts this is None.
        "pi_platform_root_message_id": pa.Column(pa.String, nullable=True),
        "pi_text": pa.Column(pa.String, nullable=True),
        "pi_platform_message_url": pa.Column(pa.String, nullable=True),
        "platform_message_last_updated_at": pipeline_jobs_utils.utc_datetime_column(
            nullable=False
        ),
        # Hash of `pi_platform_message_id`.
        "phoenix_platform_message_id": pa.Column(pa.String, nullable=False),
        # Hash of `pi_platform_message_author_id`.
        "phoenix_platform_message_author_id": pa.Column(pa.String, nullable=False),
        # Note, no version of the author name, as the id serves as the non-pi identifier.
        # Hash of `pi_platform_parent_message_id`.
        "phoenix_platform_parent_message_id": pa.Column(pa.String, nullable=True),
        "phoenix_platform_root_message_id": pa.Column(pa.String, nullable=True),
    }
)


classified_messages_schema = pa.DataFrameSchema(
    {
        "classifier_id": pa.Column(pa.Int, nullable=False),
        "class_id": pa.Column(pa.Int, nullable=False),
        "phoenix_platform_message_id": pa.Column(pa.String, nullable=False),
        "job_run_id": pa.Column(pa.Int, nullable=False),
    }
)
