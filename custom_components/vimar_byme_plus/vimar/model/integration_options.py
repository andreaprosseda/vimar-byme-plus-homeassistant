"""Runtime options bundle flowing through the data pipeline.

A single immutable container materialised by `Coordinator` from the HA
`config_entry.options` and passed down `VimarClient.retrieve_data` →
`VimarDataMapper` → individual mappers. Adding a new user-controlled
option means: new field here, populate it in `Coordinator.options`, and
read it from the consuming mapper. No signature changes downstream.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntegrationOptions:
    """Materialised values for every OptionsFlow section."""

    counter_types: dict[str, str] = field(default_factory=dict)
    # Per-device auto-refresh interval (seconds) for the
    # SFE_Cmd_TimedDynamicMode trigger. Keyed by device idsf as str.
    # 0 (or absent) = disabled — preserves zero-regression on upgrade.
    realtime_intervals: dict[str, int] = field(default_factory=dict)
    # Tolerance (percent) used to treat near-fully-closed positions as fully
    # closed when slat/tilt updates are present. Configurable via OptionsFlow.
    # Default 0 preserves existing behaviour.
    tilt_tolerance: int = 0
