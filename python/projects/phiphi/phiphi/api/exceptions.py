"""Phiphi API custom exception."""

import fastapi


class ProjectNotFound(fastapi.HTTPException):
    """Custom exception for null projects."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Project not found")


class EnvironmentNotFound(fastapi.HTTPException):
    """Custom exception for null environment."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Environment not found")


class GatherNotFound(fastapi.HTTPException):
    """Custom exception for null gather."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Gather not found")


class GatherHasActiveJobRun(fastapi.HTTPException):
    """Custom exception for gathers that have an active job run."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Gather has an active job run")
