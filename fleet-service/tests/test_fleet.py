import pytest

from fleet_service.fleet import (
    AKKU_SCHWELLE,
    IN_FAHRT,
    VERFUEGBAR,
    WARTUNG,
    Scooter,
    StatusUngueltigError,
    berechne_status,
    setze_status,
)


def test_akku_unter_schwelle_erzwingt_wartung():
    assert berechne_status(10, VERFUEGBAR) == WARTUNG


def test_akku_ueber_schwelle_behaelt_status():
    assert berechne_status(80, VERFUEGBAR) == VERFUEGBAR


def test_schwellenwert_ist_exklusiv():
    assert berechne_status(AKKU_SCHWELLE, VERFUEGBAR) == VERFUEGBAR
    assert berechne_status(AKKU_SCHWELLE - 1, VERFUEGBAR) == WARTUNG


def test_ungueltiger_status_wirft_fehler():
    with pytest.raises(StatusUngueltigError):
        berechne_status(80, "KAPUTT")


def test_setze_status_gibt_neuen_scooter_zurueck():
    scooter = Scooter(id="s1", akku=80, status=VERFUEGBAR, position=(48.2, 11.5))

    neuer_scooter = setze_status(scooter, IN_FAHRT)

    assert neuer_scooter.status == IN_FAHRT
    assert scooter.status == VERFUEGBAR
    assert neuer_scooter is not scooter


def test_setze_status_erzwingt_wartung_bei_niedrigem_akku():
    scooter = Scooter(id="s2", akku=10, status=WARTUNG, position=(48.2, 11.5))

    neuer_scooter = setze_status(scooter, VERFUEGBAR)

    assert neuer_scooter.status == WARTUNG
