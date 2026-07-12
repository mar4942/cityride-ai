from dataclasses import dataclass


@dataclass(frozen=True)
class Scooter:
    id: str
    akku: int
    status: str
