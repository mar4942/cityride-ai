from dataclasses import dataclass
from datetime import datetime

GESTARTET = "GESTARTET"
BEENDET = "BEENDET"


class ScooterNichtVerfuegbarError(Exception):
    def __init__(self, scooter_id: str):
        self.scooter_id = scooter_id
        super().__init__(f"Scooter nicht verfuegbar: {scooter_id}")


class FahrtBereitsBeendetError(Exception):
    def __init__(self, fahrt_id: str):
        self.fahrt_id = fahrt_id
        super().__init__(f"Fahrt bereits beendet: {fahrt_id}")


@dataclass(frozen=True)
class Fahrt:
    fahrt_id: str
    scooter_id: str
    fahrer_id: str
    status: str
    start_zeit: datetime


def starte_fahrt(
    fahrt_id: str,
    scooter_id: str,
    fahrer_id: str,
    scooter_verfuegbar: bool,
    start_zeit: datetime,
) -> Fahrt:
    """Startet eine Fahrt, wenn der Scooter verfuegbar ist.

    Wirft ScooterNichtVerfuegbarError sonst. Reine Funktion, keine I/O.
    """
    if not scooter_verfuegbar:
        raise ScooterNichtVerfuegbarError(scooter_id)
    return Fahrt(
        fahrt_id=fahrt_id,
        scooter_id=scooter_id,
        fahrer_id=fahrer_id,
        status=GESTARTET,
        start_zeit=start_zeit,
    )


def beende_fahrt(fahrt: Fahrt) -> Fahrt:
    """Gibt eine neue Fahrt mit Status BEENDET zurueck.

    Wirft FahrtBereitsBeendetError, wenn die Fahrt nicht mehr GESTARTET ist.
    Reine Funktion, keine I/O.
    """
    if fahrt.status != GESTARTET:
        raise FahrtBereitsBeendetError(fahrt.fahrt_id)
    return Fahrt(
        fahrt_id=fahrt.fahrt_id,
        scooter_id=fahrt.scooter_id,
        fahrer_id=fahrt.fahrer_id,
        status=BEENDET,
        start_zeit=fahrt.start_zeit,
    )


def berechne_minuten(start_zeit: datetime, ende_zeit: datetime) -> int:
    """Fahrtdauer in vollen Minuten (aufgerundet). Reine Funktion, keine I/O."""
    sekunden = (ende_zeit - start_zeit).total_seconds()
    return max(0, -(-int(sekunden) // 60))
