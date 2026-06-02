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
