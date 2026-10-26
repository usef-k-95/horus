"""Pydantic models for every record type. Collection name → model in `COLLECTIONS`."""

from .common import Envelope, Link
from .enums import *  # noqa: F401,F403
from .records import COLLECTIONS, SINGLETONS, PREFIXES, model_for

__all__ = ["Envelope", "Link", "COLLECTIONS", "SINGLETONS", "PREFIXES", "model_for"]
