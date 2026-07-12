from dataclasses import dataclass, field

from dashboard_ui.models import Scooter


@dataclass
class FakeFleetPort:
    scooters: list[Scooter] = field(default_factory=list)

    def list_scooters(self) -> list[Scooter]:
        return self.scooters
