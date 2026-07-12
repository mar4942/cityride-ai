from datetime import datetime, timedelta

import pytest

from trip_service.trip import (
    BEENDET,
    GESTARTET,
    Fahrt,
    FahrtBereitsBeendetError,
    ScooterNichtVerfuegbarError,
    beende_fahrt,
    berechne_minuten,
    starte_fahrt,
)

START_ZEIT = datetime(2026, 1, 1, 12, 0, 0)


def test_starte_fahrt_liefert_status_gestartet():
    fahrt = starte_fahrt(
        fahrt_id="f1",
        scooter_id="s1",
        fahrer_id="d1",
        scooter_verfuegbar=True,
        start_zeit=START_ZEIT,
    )

    assert fahrt.fahrt_id == "f1"
    assert fahrt.status == GESTARTET


def test_starte_fahrt_scooter_nicht_verfuegbar_wirft_fehler():
    with pytest.raises(ScooterNichtVerfuegbarError):
        starte_fahrt(
            fahrt_id="f1",
            scooter_id="s1",
            fahrer_id="d1",
            scooter_verfuegbar=False,
            start_zeit=START_ZEIT,
        )


def test_beende_fahrt_setzt_status_beendet():
    fahrt = Fahrt(
        fahrt_id="f1", scooter_id="s1", fahrer_id="d1", status=GESTARTET, start_zeit=START_ZEIT
    )

    neue_fahrt = beende_fahrt(fahrt)

    assert neue_fahrt.status == BEENDET
    assert fahrt.status == GESTARTET
    assert neue_fahrt is not fahrt


def test_beende_fahrt_bereits_beendet_wirft_fehler():
    fahrt = Fahrt(
        fahrt_id="f1", scooter_id="s1", fahrer_id="d1", status=BEENDET, start_zeit=START_ZEIT
    )

    with pytest.raises(FahrtBereitsBeendetError):
        beende_fahrt(fahrt)


def test_berechne_minuten_volle_minuten():
    ende_zeit = START_ZEIT + timedelta(minutes=10)
    assert berechne_minuten(START_ZEIT, ende_zeit) == 10


def test_berechne_minuten_rundet_auf():
    ende_zeit = START_ZEIT + timedelta(minutes=9, seconds=1)
    assert berechne_minuten(START_ZEIT, ende_zeit) == 10


def test_berechne_minuten_ohne_verstrichene_zeit():
    assert berechne_minuten(START_ZEIT, START_ZEIT) == 0
