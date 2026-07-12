from pricing_service.pricing import berechne_betrag


def test_standard_10min():
    assert berechne_betrag(10, "STANDARD", True) == 300


def test_innenstadt_10min():
    assert berechne_betrag(10, "INNENSTADT", True) == 350


def test_geofence_verletzt():
    assert berechne_betrag(10, "STANDARD", False) == 800


def test_innenstadt_und_geofence_verletzt():
    assert berechne_betrag(10, "INNENSTADT", False) == 850
