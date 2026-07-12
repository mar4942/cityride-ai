from fastapi.testclient import TestClient

from geofence_service import api
from geofence_service.geofence import MAX_LAT, MAX_LNG, MIN_LAT, MIN_LNG

client = TestClient(api.app)


def test_pruefen_punkt_in_zone():
    mitte_lat = (MIN_LAT + MAX_LAT) / 2
    mitte_lng = (MIN_LNG + MAX_LNG) / 2

    response = client.post("/pruefen", json={"lat": mitte_lat, "lng": mitte_lng})

    assert response.status_code == 200
    assert response.json() == {"in_zone": True, "zone": "STADTGEBIET"}


def test_pruefen_punkt_ausserhalb():
    response = client.post("/pruefen", json={"lat": MIN_LAT - 1, "lng": MIN_LNG - 1})

    assert response.status_code == 200
    assert response.json() == {"in_zone": False, "zone": "AUSSERHALB"}


def test_pruefen_ungueltiges_payload():
    response = client.post("/pruefen", json={"lat": "keine-zahl", "lng": 11.5})

    assert response.status_code == 422
