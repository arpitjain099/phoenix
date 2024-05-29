"""Tables schemas for the project database."""
import pandera as pa

# Schema for gather batches
gather_batches_schema = pa.DataFrameSchema(
    {
        "project_id": pa.Column(pa.Int, nullable=False),
        "gather_id": pa.Column(pa.Int, nullable=False),
        "job_run_id": pa.Column(pa.Int, nullable=False),
        "source": pa.Column(pa.String, checks=pa.Check.isin(["apify"]), nullable=False),
        "platform": pa.Column(
            pa.String,
            checks=pa.Check.isin(["facebook", "instagram", "tiktok", "x-twitter"]),
            nullable=False,
        ),
        "data_type": pa.Column(
            pa.String, checks=pa.Check.isin(["post", "comment"]), nullable=False
        ),
        "batch_id": pa.Column(pa.Int, nullable=False),
        "batch_created_at": pa.Column(pa.DateTime, nullable=False),
        "json_data": pa.Column(pa.String, nullable=False),
        "last_processed_at": pa.Column(pa.DateTime, nullable=True),
    }
)


# Schema that all messages (of any type and any source) should be normalised to
generalised_messages_schema = pa.DataFrameSchema(
    {
        "project_id": pa.Column(pa.Int, nullable=False),
        "gather_id": pa.Column(pa.Int, nullable=False),
        "gather_batch_id": pa.Column(pa.Int, nullable=False),
        "gathered_at": pa.Column(pa.DateTime, nullable=False),
        "phoenix_processed_at": pa.Column(pa.DateTime, nullable=False),
        "source": pa.Column(pa.String, checks=pa.Check.isin(["apify"]), nullable=False),
        # NOTE: combination of (platform, data_type, pi_platform_message_id) should give a unique
        # message, but it won't be a unique row as we process the same message multiple times.
        # Doing groupby on these columns then getting MAX(phoenix_processed_at) will give the
        # latest set of unique messages. `phoenix_platform_message_id` can be used instead of
        # `pi_platform_message_id` in the groupby also.
        "platform": pa.Column(
            pa.String,
            checks=pa.Check.isin(["facebook", "instagram", "tiktok", "x-twitter"]),
            nullable=False,
        ),
        "data_type": pa.Column(
            pa.String, checks=pa.Check.isin(["post", "comment"]), nullable=False
        ),
        "pi_platform_message_id": pa.Column(nullable=True),
        "pi_platform_message_author_id": pa.Column(nullable=True),
        "pi_platform_message_author_name": pa.Column(pa.String, nullable=True),
        "pi_platform_parent_message_id": pa.Column(nullable=True),
        "pi_text": pa.Column(pa.String, nullable=True),
        "pi_platform_message_url": pa.Column(pa.String, nullable=True),
        "platform_message_last_updated_at": pa.Column(pa.DateTime, nullable=False),
        # Hash of `pi_platform_message_id`.
        "phoenix_platform_message_id": pa.Column(pa.String, nullable=False),
        # Hash of `pi_platform_message_author_id`.
        "phoenix_platform_message_author_id": pa.Column(pa.String, nullable=False),
        # Note, no version of the author name, as the id serves as the non-pi identifier.
        # Hash of `pi_platform_parent_message_id`.
        "phoenix_platform_parent_message_id": pa.Column(pa.String, nullable=True),
    }
)
