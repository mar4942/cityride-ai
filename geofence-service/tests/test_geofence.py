from geofence_service.geofence import (
    MAX_LAT,
    MAX_LNG,
    MIN_LAT,
    MIN_LNG,
    ZONE_AUSSERHALB,
    ZONE_NAME,
    pruefe_punkt,
)


def test_punkt_in_der_zone():
    mitte_lat = (MIN_LAT + MAX_LAT) / 2
    mitte_lng = (MIN_LNG + MAX_LNG) / 2
    assert pruefe_punkt(mitte_lat, mitte_lng) == (True, ZONE_NAME)


def test_punkt_ausserhalb_lat_zu_klein():
    assert pruefe_punkt(MIN_LAT - 1, MIN_LNG) == (False, ZONE_AUSSERHALB)


def test_punkt_ausserhalb_lat_zu_gross():
    assert pruefe_punkt(MAX_LAT + 1, MIN_LNG) == (False, ZONE_AUSSERHALB)


def test_punkt_ausserhalb_lng_zu_klein():
    assert pruefe_punkt(MIN_LAT, MIN_LNG - 1) == (False, ZONE_AUSSERHALB)


def test_punkt_ausserhalb_lng_zu_gross():
    assert pruefe_punkt(MIN_LAT, MAX_LNG + 1) == (False, ZONE_AUSSERHALB)


def test_randpunkte_sind_inklusive():
    assert pruefe_punkt(MIN_LAT, MIN_LNG) == (True, ZONE_NAME)
    assert pruefe_punkt(MAX_LAT, MAX_LNG) == (True, ZONE_NAME)
