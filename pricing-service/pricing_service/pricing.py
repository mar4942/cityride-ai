GRUNDGEBUEHR_CENT = 100
PREIS_PRO_MINUTE_CENT = 20
ZONE_INNENSTADT = "INNENSTADT"
ZONENZUSCHLAG_CENT = 50
STRAFGEBUEHR_GEOFENCE_CENT = 500


def berechne_betrag(minuten: int, zone: str, geofence_ok: bool) -> int:
    """Betrag in Cent nach den Fachregeln. Reine Funktion, keine I/O."""
    betrag = GRUNDGEBUEHR_CENT + PREIS_PRO_MINUTE_CENT * minuten
    if zone == ZONE_INNENSTADT:
        betrag += ZONENZUSCHLAG_CENT
    if not geofence_ok:
        betrag += STRAFGEBUEHR_GEOFENCE_CENT
    return betrag
