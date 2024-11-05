"""Base schemas."""
import pydantic


class ListMeta(pydantic.BaseModel):
    """List meta schema."""

    total_count: int = pydantic.Field(..., description="The total count of items.")
