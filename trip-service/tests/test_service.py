from datetime import datetime, timedelta

import pytest

from tests.fakes import FakeFleetPort, FakePricingPort
from trip_service.service import FahrtNichtGefundenError, FahrtService
from trip_service.trip import BEENDET, FahrtBereitsBeendetError, ScooterNichtVerfuegbarError

START_ZEIT = datetime(2026, 1, 1, 12, 0, 0)


def _service(fleet=None, pricing=None, zeiten=None):
    fleet = fleet or FakeFleetPort(verfuegbar={"s1": True})
    pricing = pricing or FakePricingPort(betrag=300, wallet_saldo=700)
    ticks = iter(zeiten or [START_ZEIT])
    return FahrtService(fleet=fleet, pricing=pricing, now=lambda: next(ticks)), fleet, pricing


def test_start_liefert_fahrt_mit_status_gestartet():
    service, fleet, _ = _service()

    fahrt = service.start("s1", "d1")

    assert fahrt.status == "GESTARTET"
    assert fleet.angefragt == ["s1"]


def test_start_scooter_nicht_verfuegbar_wirft_fehler():
    service, _, _ = _service(fleet=FakeFleetPort(verfuegbar={"s1": False}))

    with pytest.raises(ScooterNichtVerfuegbarError):
        service.start("s1", "d1")


def test_beenden_unbekannte_fahrt_wirft_fehler():
    service, _, _ = _service()

    with pytest.raises(FahrtNichtGefundenError):
        service.beenden("unbekannt", zone="STANDARD", geofence_ok=True)


def test_beenden_setzt_status_beendet_und_liefert_betrag():
    ende_zeit = START_ZEIT + timedelta(minutes=10)
    service, _, pricing = _service(zeiten=[START_ZEIT, ende_zeit])

    service.start("s1", "d1")
    fahrt_id = next(iter(service._fahrten))

    fahrt, betrag = service.beenden(fahrt_id, zone="STANDARD", geofence_ok=True)

    assert fahrt.status == BEENDET
    assert betrag == 300
    assert pricing.aufrufe == [
        {"fahrt_id": fahrt_id, "minuten": 10, "zone": "STANDARD", "geofence_ok": True}
    ]


def test_beenden_bereits_beendete_fahrt_wirft_fehler():
    service, _, _ = _service(zeiten=[START_ZEIT, START_ZEIT, START_ZEIT])

    service.start("s1", "d1")
    fahrt_id = next(iter(service._fahrten))
    service.beenden(fahrt_id, zone="STANDARD", geofence_ok=True)

    with pytest.raises(FahrtBereitsBeendetError):
        service.beenden(fahrt_id, zone="STANDARD", geofence_ok=True)


def test_beenden_wallet_unterdeckung_laesst_fahrt_gestartet():
    from trip_service.ports import WalletUnterdeckungError

    service, _, _ = _service(
        pricing=FakePricingPort(wallet_unterdeckt=True), zeiten=[START_ZEIT, START_ZEIT]
    )

    service.start("s1", "d1")
    fahrt_id = next(iter(service._fahrten))

    with pytest.raises(WalletUnterdeckungError):
        service.beenden(fahrt_id, zone="STANDARD", geofence_ok=True)

    assert service._fahrten[fahrt_id].status == "GESTARTET"
