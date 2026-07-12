import pytest
from fastapi.testclient import TestClient

from pricing_service import api
from pricing_service.wallet import Wallet

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def _reset_wallets():
    api._wallets.clear()
    yield
    api._wallets.clear()


def test_abrechnen_standard_10min():
    response = client.post(
        "/abrechnen",
        json={"fahrt_id": "f1", "minuten": 10, "zone": "STANDARD", "geofence_ok": True},
    )
    assert response.status_code == 200
    assert response.json() == {"betrag": 300, "wallet_saldo": 700}


def test_abrechnen_innenstadt_10min():
    response = client.post(
        "/abrechnen",
        json={"fahrt_id": "f2", "minuten": 10, "zone": "INNENSTADT", "geofence_ok": True},
    )
    assert response.status_code == 200
    assert response.json()["betrag"] == 350


def test_abrechnen_geofence_verletzt():
    response = client.post(
        "/abrechnen",
        json={"fahrt_id": "f3", "minuten": 10, "zone": "STANDARD", "geofence_ok": False},
    )
    assert response.status_code == 200
    assert response.json()["betrag"] == 800


def test_abrechnen_wallet_unterdeckung():
    api._wallets["f4"] = Wallet(saldo_cent=100)

    response = client.post(
        "/abrechnen",
        json={"fahrt_id": "f4", "minuten": 10, "zone": "STANDARD", "geofence_ok": False},
    )

    assert response.status_code == 402
    assert api._wallets["f4"].saldo_cent == 100


def test_abrechnen_neue_fahrt_startet_mit_default_saldo():
    response = client.post(
        "/abrechnen",
        json={"fahrt_id": "f5", "minuten": 10, "zone": "STANDARD", "geofence_ok": True},
    )
    assert response.status_code == 200
    assert response.json()["wallet_saldo"] == api.STARTGUTHABEN_CENT - 300
