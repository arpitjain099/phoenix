"""Tables schemas for the project database."""
import pandera as pa

from phiphi.api.projects.gathers import schemas


def utc_datetime_column(nullable: bool) -> pa.Column:
    """Return a Pandera column for a UTC datetime which coerces.

    Should be used for columns that are expected to be UTC datetimes, and dfs should be passed
    through validation to ensure columns are coerced.
    """
    return pa.Column(
        pa.engines.pandas_engine.DateTime(  # type: ignore[call-arg]
            unit="ms",
            tz="UTC",
        ),
        coerce=True,
        nullable=nullable,
    )


# Schema for gather batches
gather_batches_schema = pa.DataFrameSchema(
    {
        "gather_id": pa.Column(pa.Int, nullable=False),
        "job_run_id": pa.Column(pa.Int, nullable=False),
        "source": pa.Column(
            pa.String, checks=pa.Check.isin([e.value for e in schemas.Source]), nullable=False
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
        "gathered_at": utc_datetime_column(nullable=False),
        "json_data": pa.Column(pa.String, nullable=False),
        "last_processed_at": utc_datetime_column(nullable=True),
    }
)


# Schema that all messages (of any type and any source) should be normalised to
generalised_messages_schema = pa.DataFrameSchema(
    {
        "gather_id": pa.Column(pa.Int, nullable=False),
        "gather_batch_id": pa.Column(pa.Int, nullable=False),
        "gathered_at": utc_datetime_column(nullable=False),
        "phoenix_processed_at": utc_datetime_column(nullable=False),
        "source": pa.Column(
            pa.String, checks=pa.Check.isin([e.value for e in schemas.Source]), nullable=False
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
        "pi_platform_message_id": pa.Column(nullable=True),
        "pi_platform_message_author_id": pa.Column(nullable=True),
        "pi_platform_message_author_name": pa.Column(pa.String, nullable=True),
        "pi_platform_parent_message_id": pa.Column(nullable=True),
        "pi_text": pa.Column(pa.String, nullable=True),
        "pi_platform_message_url": pa.Column(pa.String, nullable=True),
        "platform_message_last_updated_at": utc_datetime_column(nullable=False),
        # Hash of `pi_platform_message_id`.
        "phoenix_platform_message_id": pa.Column(pa.String, nullable=False),
        # Hash of `pi_platform_message_author_id`.
        "phoenix_platform_message_author_id": pa.Column(pa.String, nullable=False),
        # Note, no version of the author name, as the id serves as the non-pi identifier.
        # Hash of `pi_platform_parent_message_id`.
        "phoenix_platform_parent_message_id": pa.Column(pa.String, nullable=True),
    }
)
