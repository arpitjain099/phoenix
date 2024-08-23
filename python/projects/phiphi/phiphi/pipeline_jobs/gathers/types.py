"""Gather pipelines types."""
import dataclasses


@dataclasses.dataclass
class ScrapeResponse:
    """Response from a scrape in a gather."""

    total_items: int
    total_batches: int
