MIN_LAT = 48.10
MAX_LAT = 48.30
MIN_LNG = 11.45
MAX_LNG = 11.70

ZONE_NAME = "STADTGEBIET"
ZONE_AUSSERHALB = "AUSSERHALB"


def pruefe_punkt(lat: float, lng: float) -> tuple[bool, str]:
    """Prueft, ob (lat, lng) im Rechteck liegt. Reine Funktion, keine I/O."""
    in_zone = MIN_LAT <= lat <= MAX_LAT and MIN_LNG <= lng <= MAX_LNG
    zone = ZONE_NAME if in_zone else ZONE_AUSSERHALB
    return in_zone, zone
