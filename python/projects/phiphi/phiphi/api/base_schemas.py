"""Base schemas for the API."""
from enum import Enum


class RunStatus(str, Enum):
    """Base Run Status."""

    in_queue = "in_queue"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    yet_to_run = "yet_to_run"
