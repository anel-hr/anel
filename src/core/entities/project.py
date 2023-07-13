import datetime as dt

from pydantic import BaseModel, Field

from src.core.entities.shared import Status


class ProjectEntity(BaseModel):
    """
    ProjectEntity is the entity that is used to represent a project in the application
    """

    id: int = Field(..., description="Unique identifier for the project")
    name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Description of the project")
    status: str = Field(..., description="Status of the project")
    created_at: dt.datetime | None = Field(..., description="Date and time when the project was created")
    updated_at: dt.datetime | None = Field(..., description="Date and time when the project was modified")

    def activate(self) -> None:
        """Activates the user."""

        self.status = Status.ACTIVE
        self.updated_at = dt.datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivates the user."""

        self.status = Status.INACTIVE
        self.updated_at = dt.datetime.utcnow()
