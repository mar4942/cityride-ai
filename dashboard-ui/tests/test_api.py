import pytest
from fastapi.testclient import TestClient

from dashboard_ui import api
from dashboard_ui.models import Scooter
from tests.fakes import FakeFleetPort

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def _reset_overrides():
    yield
    api.app.dependency_overrides.clear()


def _override(scooters: list[Scooter]) -> None:
    api.app.dependency_overrides[api.get_fleet_port] = lambda: FakeFleetPort(scooters=scooters)


def test_dashboard_zeigt_alle_scooter():
    _override(
        [
            Scooter(id="scooter-1", akku=80, status="VERFUEGBAR"),
            Scooter(id="scooter-2", akku=10, status="WARTUNG"),
        ]
    )

    response = client.get("/")

    assert response.status_code == 200
    assert "scooter-1" in response.text
    assert "scooter-2" in response.text


def test_dashboard_hebt_wartung_hervor():
    _override([Scooter(id="scooter-2", akku=10, status="WARTUNG")])

    response = client.get("/")

    assert 'class="wartung"' in response.text
