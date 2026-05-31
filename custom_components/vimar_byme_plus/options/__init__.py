"""Section registry for the OptionsFlow."""

from .base import OptionsSection
from .counters import CountersSection

SECTIONS: tuple[type[OptionsSection], ...] = (CountersSection,)

__all__ = ["OptionsSection", "SECTIONS"]
