"""Section registry for the OptionsFlow."""

from .base import OptionsSection
from .counters import CountersSection
from .realtime import RealtimeSection

SECTIONS: tuple[type[OptionsSection], ...] = (
    CountersSection,
    RealtimeSection,
)

__all__ = ["OptionsSection", "SECTIONS"]
