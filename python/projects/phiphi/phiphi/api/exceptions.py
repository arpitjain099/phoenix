"""Phiphi API custom exception."""

import fastapi


class InstanceNotFound(fastapi.HTTPException):
    """Custom exception for null instances."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Instance not found")


class EnvironmentNotFound(fastapi.HTTPException):
    """Custom exception for null environment."""

    def __init__(self) -> None:
        """Constructor for custom exception."""
        super().__init__(status_code=400, detail="Environment not found")
