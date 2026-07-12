import pytest
from fastapi.testclient import TestClient

from tests.fakes import FakeFleetPort, FakePricingPort
from trip_service import api
from trip_service.service import FahrtService

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def _reset_overrides():
    yield
    api.app.dependency_overrides.clear()


def _override(fleet=None, pricing=None):
    fleet = fleet or FakeFleetPort(verfuegbar={"s1": True})
    pricing = pricing or FakePricingPort(betrag=300, wallet_saldo=700)
    service = FahrtService(fleet=fleet, pricing=pricing)
    api.app.dependency_overrides[api.get_fahrt_service] = lambda: service
    return service


def test_start_liefert_fahrt_id_und_status_gestartet():
    _override()

    response = client.post("/fahrt/start", json={"scooter_id": "s1", "fahrer_id": "d1"})

    assert response.status_code == 200
    body = response.json()
    assert "fahrt_id" in body
    assert body["status"] == "GESTARTET"


def test_start_scooter_nicht_verfuegbar_409():
    _override(fleet=FakeFleetPort(verfuegbar={"s1": False}))

    response = client.post("/fahrt/start", json={"scooter_id": "s1", "fahrer_id": "d1"})

    assert response.status_code == 409


def test_beenden_setzt_status_beendet_und_liefert_betrag():
    _override(pricing=FakePricingPort(betrag=350, wallet_saldo=650))

    start_response = client.post("/fahrt/start", json={"scooter_id": "s1", "fahrer_id": "d1"})
    fahrt_id = start_response.json()["fahrt_id"]

    response = client.post(
        f"/fahrt/{fahrt_id}/beenden", json={"zone": "INNENSTADT", "geofence_ok": True}
    )

    assert response.status_code == 200
    assert response.json() == {"status": "BEENDET", "betrag": 350}


def test_beenden_unbekannte_fahrt_404():
    _override()

    response = client.post(
        "/fahrt/unbekannt/beenden", json={"zone": "STANDARD", "geofence_ok": True}
    )

    assert response.status_code == 404


def test_beenden_bereits_beendete_fahrt_409():
    _override()

    start_response = client.post("/fahrt/start", json={"scooter_id": "s1", "fahrer_id": "d1"})
    fahrt_id = start_response.json()["fahrt_id"]
    client.post(f"/fahrt/{fahrt_id}/beenden", json={"zone": "STANDARD", "geofence_ok": True})

    response = client.post(
        f"/fahrt/{fahrt_id}/beenden", json={"zone": "STANDARD", "geofence_ok": True}
    )

    assert response.status_code == 409


def test_beenden_wallet_unterdeckung_402():
    _override(pricing=FakePricingPort(wallet_unterdeckt=True))

    start_response = client.post("/fahrt/start", json={"scooter_id": "s1", "fahrer_id": "d1"})
    fahrt_id = start_response.json()["fahrt_id"]

    response = client.post(
        f"/fahrt/{fahrt_id}/beenden", json={"zone": "STANDARD", "geofence_ok": True}
    )

    assert response.status_code == 402
