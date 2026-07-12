from dataclasses import dataclass

VERFUEGBAR = "VERFUEGBAR"
RESERVIERT = "RESERVIERT"
IN_FAHRT = "IN_FAHRT"
WARTUNG = "WARTUNG"
LADEN = "LADEN"
OFFLINE = "OFFLINE"

STATUS_WERTE = {VERFUEGBAR, RESERVIERT, IN_FAHRT, WARTUNG, LADEN, OFFLINE}

AKKU_SCHWELLE = 15


class StatusUngueltigError(Exception):
    def __init__(self, status: str):
        self.status = status
        super().__init__(f"Ungueltiger Status: {status}")


@dataclass(frozen=True)
class Scooter:
    id: str
    akku: int
    status: str
    position: tuple[float, float]


def berechne_status(akku: int, angeforderter_status: str) -> str:
    """Wendet die Akku-Regel auf einen angeforderten Status an.

    akku < 15 -> immer WARTUNG, nicht mehr vermittelbar.
    Reine Funktion, keine I/O.
    """
    if angeforderter_status not in STATUS_WERTE:
        raise StatusUngueltigError(angeforderter_status)
    if akku < AKKU_SCHWELLE:
        return WARTUNG
    return angeforderter_status


def setze_status(scooter: Scooter, angeforderter_status: str) -> Scooter:
    """Gibt einen neuen Scooter mit aktualisiertem Status zurueck."""
    neuer_status = berechne_status(scooter.akku, angeforderter_status)
    return Scooter(
        id=scooter.id,
        akku=scooter.akku,
        status=neuer_status,
        position=scooter.position,
    )
