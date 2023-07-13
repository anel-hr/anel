import datetime as dt

from pydantic import BaseModel, Field, field_validator


class CandidateEntity(BaseModel):
    """
    CandidateEntity is the entity that is used to represent a candidate in the application
    """

    id: int = Field(..., description="Unique identifier for the candidate")
    name: str = Field(..., description="Name of the candidate")
    email: str = Field(..., description="Email address of the candidate")
    phone: str = Field(..., description="Phone number of the candidate")
    skills: str = Field(..., description="Skills of the candidate")
    experience: str = Field(..., description="Experience of the candidate")
    status: str = Field(..., description="Status of the candidate")
    created_at: dt.datetime | None = Field(..., description="Date and time when the candidate was created")
    updated_at: dt.datetime | None = Field(..., description="Date and time when the candidate was modified")

    @field_validator("status")
    def validate_status(cls, _: str, values: dict[str, str]):
        if values["status"] not in ["active", "inactive"]:
            raise ValueError("Invalid status")
