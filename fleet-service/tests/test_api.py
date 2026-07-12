import pytest
from fastapi.testclient import TestClient

from fleet_service import api

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def _reset_scooters():
    original = dict(api._scooters)
    yield
    api._scooters.clear()
    api._scooters.update(original)


def test_list_scooters_liefert_alle_scooter():
    response = client.get("/scooters")

    assert response.status_code == 200
    body = response.json()
    assert {s["id"] for s in body} == {"scooter-1", "scooter-2"}
    ids_zu_status = {s["id"]: s["status"] for s in body}
    assert ids_zu_status["scooter-1"] == "VERFUEGBAR"
    assert ids_zu_status["scooter-2"] == "WARTUNG"


def test_get_scooter_mit_akku_80_liefert_verfuegbar():
    response = client.get("/scooter/scooter-1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "scooter-1"
    assert body["akku"] == 80
    assert body["status"] == "VERFUEGBAR"
    assert body["position"] == {"lat": 48.20, "lng": 11.55}


def test_get_scooter_mit_akku_10_liefert_wartung():
    response = client.get("/scooter/scooter-2")

    assert response.status_code == 200
    body = response.json()
    assert body["akku"] == 10
    assert body["status"] == "WARTUNG"


def test_get_unbekannter_scooter_404():
    response = client.get("/scooter/unbekannt")

    assert response.status_code == 404


def test_post_status_setzt_neuen_status():
    response = client.post("/scooter/scooter-1/status", json={"status": "RESERVIERT"})

    assert response.status_code == 200
    assert response.json() == {"id": "scooter-1", "status": "RESERVIERT"}

    folge_response = client.get("/scooter/scooter-1")
    assert folge_response.json()["status"] == "RESERVIERT"


def test_post_status_bei_niedrigem_akku_bleibt_wartung():
    response = client.post("/scooter/scooter-2/status", json={"status": "VERFUEGBAR"})

    assert response.status_code == 200
    assert response.json() == {"id": "scooter-2", "status": "WARTUNG"}


def test_post_status_unbekannter_scooter_404():
    response = client.post("/scooter/unbekannt/status", json={"status": "VERFUEGBAR"})

    assert response.status_code == 404


def test_post_status_ungueltiger_wert_422():
    response = client.post("/scooter/scooter-1/status", json={"status": "KAPUTT"})

    assert response.status_code == 422
