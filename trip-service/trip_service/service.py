from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4

from trip_service import trip
from trip_service.ports import FleetPort, PricingPort
from trip_service.trip import Fahrt


class FahrtNichtGefundenError(Exception):
    def __init__(self, fahrt_id: str):
        self.fahrt_id = fahrt_id
        super().__init__(f"Fahrt nicht gefunden: {fahrt_id}")


class FahrtService:
    """Orchestriert den Fahrt-Lebenszyklus ueber die injizierten Ports.

    Kennt keine HTTP-Details, nur FleetPort/PricingPort-Abstraktionen.
    """

    def __init__(
        self,
        fleet: FleetPort,
        pricing: PricingPort,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ):
        self._fleet = fleet
        self._pricing = pricing
        self._now = now
        self._fahrten: dict[str, Fahrt] = {}

    def start(self, scooter_id: str, fahrer_id: str) -> Fahrt:
        verfuegbar = self._fleet.ist_verfuegbar(scooter_id)
        fahrt = trip.starte_fahrt(
            fahrt_id=str(uuid4()),
            scooter_id=scooter_id,
            fahrer_id=fahrer_id,
            scooter_verfuegbar=verfuegbar,
            start_zeit=self._now(),
        )
        self._fahrten[fahrt.fahrt_id] = fahrt
        return fahrt

    def beenden(self, fahrt_id: str, zone: str, geofence_ok: bool) -> tuple[Fahrt, int]:
        fahrt = self._fahrten.get(fahrt_id)
        if fahrt is None:
            raise FahrtNichtGefundenError(fahrt_id)

        minuten = trip.berechne_minuten(fahrt.start_zeit, self._now())
        ergebnis = self._pricing.abrechnen(
            fahrt_id=fahrt_id, minuten=minuten, zone=zone, geofence_ok=geofence_ok
        )
        neue_fahrt = trip.beende_fahrt(fahrt)
        self._fahrten[fahrt_id] = neue_fahrt
        return neue_fahrt, ergebnis.betrag
