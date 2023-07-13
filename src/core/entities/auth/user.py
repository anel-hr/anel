import datetime as dt
import secrets
from uuid import UUID

import bcrypt
from pydantic import BaseModel, Field, field_validator

from src.core.entities.shared import Status
from src.core.exceptions.auth_exceptions import InvalidCredentialsError


class UserEntity(BaseModel):
    """
    UserEntity is the entity that is used to represent a user in the application
    """

    id: UUID = Field(..., description="Unique identifier for the user")
    status: Status = Field(..., description="Status of the user")

    default_project_id: UUID = Field(..., description="Default project ID of the user")

    email: str = Field(..., description="Email address of the user")
    password: str = Field(..., description="Hashed password of the user")

    created_at: dt.datetime | None = Field(None, description="Date and time when the user was created")
    updated_at: dt.datetime | None = Field(None, description="Date and time when the user was modified")

    def activate(self) -> None:
        """Activates the user."""

        self.status = Status.ACTIVE
        self.updated_at = dt.datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivates the user."""

        self.status = Status.INACTIVE
        self.updated_at = dt.datetime.utcnow()


class UserCredentials(BaseModel):
    """
    UserCredentials is the entity that is used to represent a user credentials
    """

    email: str = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")
    hashed_password: str | None = Field(None, description="Hashed password of the user")
    confirmation_token: str | None = Field(None, description="Confirmation token of the user")

    @field_validator("hashed_password")
    def validate_password(cls, _: str, values: dict[str, str | None]) -> str:  # noqa: N805
        if not values["password"]:
            raise InvalidCredentialsError

        salt = bcrypt.gensalt()
        hashed_password: str = bcrypt.hashpw(values["password"].encode("utf-8"), salt).decode("utf-8")
        return hashed_password

    @field_validator("confirmation_token")
    def generate_confirmation_token(cls, _: str) -> str:  # noqa: N805
        confirmation_token = secrets.token_urlsafe(32)
        return confirmation_token
