
from pydantic import BaseModel, ConfigDict, Field


class DomainCreate(BaseModel):
    domain: str = Field(min_length=1, max_length=253)
    ip: str = Field(min_length=8, max_length=16)
    description: str | None = Field(
        default=None,
        max_length=500
    )


class DomainUpdate(BaseModel):
    domain: str = Field(min_length=1, max_length=253)
    ip: str = Field(min_length=8, max_length=16)
    description: str | None = Field(
        default=None,
        max_length=500
    )


class DomainResponse(BaseModel):
    id: int
    domain: str
    ip: str = Field(min_length=8, max_length=16)
    description: str | None

    model_config = ConfigDict(from_attributes=True)
