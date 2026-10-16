from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class EventResponse(BaseModel):
    id: str
    slug: str
    title: str
    summary: str
    location: str
    starts_at: str
    capacity: int
    minimum_age: int
    status: Literal["published"]
    confirmed_count: int
    waitlist_count: int
    remaining_seats: int


class RegistrationCreate(BaseModel):
    event_id: str = Field(min_length=3, max_length=80)
    attendee_name: str = Field(min_length=2, max_length=80)
    attendee_email: str = Field(min_length=5, max_length=254)
    attendee_age: int = Field(ge=0, le=120)
    consent: bool

    @field_validator("attendee_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if len(cleaned) < 2:
            raise ValueError("Name must contain at least two visible characters")
        return cleaned

    @field_validator("attendee_email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise ValueError("Enter a valid email address")
        return normalized


class RegistrationResponse(BaseModel):
    id: str
    event_id: str
    attendee_name: str
    attendee_email: str
    attendee_age: int
    consent: bool
    status: Literal["confirmed", "waitlisted", "cancelled"]
    idempotency_key: str | None = None
    created_at: str
    updated_at: str
    replayed: bool = False
    promoted_registration_id: str | None = None


class ScenarioRequest(BaseModel):
    requirement: str = Field(min_length=20, max_length=2000)
    risk: Literal["low", "medium", "high"] = "medium"

    @field_validator("requirement")
    @classmethod
    def normalize_requirement(cls, value: str) -> str:
        return " ".join(value.split())


class Scenario(BaseModel):
    id: str = Field(min_length=2, max_length=40)
    title: str = Field(min_length=5, max_length=180)
    technique: str = Field(min_length=3, max_length=80)
    priority: Literal["P0", "P1", "P2"]
    steps: list[str] = Field(min_length=1, max_length=10)
    expected: str = Field(min_length=5, max_length=600)
    tags: list[str] = Field(min_length=1, max_length=10)


class ScenarioResponse(BaseModel):
    provider: str = Field(min_length=3, max_length=40)
    requirement_summary: str = Field(min_length=5, max_length=240)
    risks_detected: list[str] = Field(min_length=1, max_length=20)
    scenarios: list[Scenario] = Field(min_length=1, max_length=30)
    review_note: str = Field(min_length=10, max_length=500)
