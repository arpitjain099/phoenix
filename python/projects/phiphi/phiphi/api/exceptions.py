"""Phiphi API custom exception."""

import fastapi


class HttpException400(fastapi.HTTPException):
    """Custom exception for 400 status code."""

    def __init__(self, detail: str) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail=detail)


class ProjectNotFound(fastapi.HTTPException):
    """Custom exception for null projects."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Project not found")


class WorkspaceNotFound(fastapi.HTTPException):
    """Custom exception for null workspace."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Workspace not found")


class GatherNotFound(fastapi.HTTPException):
    """Custom exception for null gather."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Gather not found")


class ForeignObjectHasActiveJobRun(fastapi.HTTPException):
    """Custom exception for active job run on foreign object."""

    def __init__(self, foreign_id: int, foreign_job_type: str) -> None:
        """Constructor for custom exception."""
        super().__init__(
            status_code=400,
            detail=(
                "Foreign object has an active job run."
                f" Type: {foreign_job_type}, Id: {foreign_id}"
            ),
        )
