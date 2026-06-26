"""Section registry for the OptionsFlow."""

from .base import OptionsSection
from .counters import CountersSection
from .realtime import RealtimeSection
from .tilt_tolerance import TiltToleranceSection

SECTIONS: tuple[type[OptionsSection], ...] = (
    CountersSection,
    RealtimeSection,
    TiltToleranceSection,
)

__all__ = ["OptionsSection", "SECTIONS"]
