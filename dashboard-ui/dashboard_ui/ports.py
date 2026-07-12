from typing import Protocol

from dashboard_ui.models import Scooter


class FleetPort(Protocol):
    def list_scooters(self) -> list[Scooter]: ...
