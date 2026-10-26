"""Common envelope carried by every record (STATE_SCHEMA.md §2.2)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .enums import Confidentiality, Phase


class StrictModel(BaseModel):
    """Unknown fields are rejected everywhere (integrity rule 1)."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True, validate_assignment=True, validate_default=True)


class Link(StrictModel):
    rel: str
    to: str


class Envelope(StrictModel):
    id: str
    collection: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
    session_id: str = "unknown"
    status: str
    confidentiality: Confidentiality = Confidentiality.client_confidential
    created_in_phase: Optional[Phase] = None
    tags: list[str] = Field(default_factory=list)
    links: list[Link] = Field(default_factory=list)
    notes: Optional[str] = None
    schema_version: str = "0.2.0"


ENVELOPE_FIELDS = set(Envelope.model_fields)
SERVER_FIELDS = {"id", "collection", "created_at", "updated_at", "created_by", "updated_by", "session_id", "schema_version"}
