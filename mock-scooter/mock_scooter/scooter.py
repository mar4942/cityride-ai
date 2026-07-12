"""Scooter state model — holds battery, lock, and position for a simulated e-scooter."""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Scooter:
    """Represents the mutable state of a single simulated scooter.

    Every state change should be followed by a call to the
    registered callback so the change can be published via MQTT.
    """

    scooter_id: str
    battery_level: float = 100.0          # percent 0..100
    locked: bool = True
    lat: float = 48.137154                # default: Munich centre
    lng: float = 11.576124
    on_change: Optional[callable] = field(default=None, repr=False, compare=False)

    def set_battery(self, level: float) -> None:
        """Set battery level (clamped to 0‑100)."""
        self.battery_level = max(0.0, min(100.0, level))
        self._notify()

    def set_locked(self, locked: bool) -> None:
        """Lock or unlock the scooter."""
        self.locked = locked
        self._notify()

    def set_position(self, lat: float, lng: float) -> None:
        """Set geographic position."""
        self.lat = lat
        self.lng = lng
        self._notify()

    def _notify(self) -> None:
        if self.on_change:
            self.on_change(self)

    def to_dict(self) -> dict:
        return {
            "scooter_id": self.scooter_id,
            "battery_level": self.battery_level,
            "locked": self.locked,
            "lat": self.lat,
            "lng": self.lng,
        }