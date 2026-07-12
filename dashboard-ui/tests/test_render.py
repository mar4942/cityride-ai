from dashboard_ui.models import Scooter
from dashboard_ui.render import render_dashboard


def test_verfuegbarer_scooter_ohne_hervorhebung():
    html = render_dashboard([Scooter(id="scooter-1", akku=80, status="VERFUEGBAR")])

    assert "scooter-1" in html
    assert "VERFUEGBAR" in html
    assert 'class="wartung"' not in html


def test_wartung_scooter_wird_hervorgehoben():
    html = render_dashboard([Scooter(id="scooter-2", akku=10, status="WARTUNG")])

    assert '<tr class="wartung">' in html
    assert "scooter-2" in html


def test_gemischte_liste_hebt_nur_wartung_hervor():
    html = render_dashboard(
        [
            Scooter(id="scooter-1", akku=80, status="VERFUEGBAR"),
            Scooter(id="scooter-2", akku=10, status="WARTUNG"),
        ]
    )

    assert html.count('class="wartung"') == 1
