"""All Project db tables."""
from phiphi import project_db
from phiphi.pipeline_jobs import (
    gather_batches,  # noqa: F401
    tabulated_messages,  # noqa: F401
)

metadata = project_db.metadata
