from html import escape

from dashboard_ui.models import Scooter

WARTUNG = "WARTUNG"


def render_dashboard(scooters: list[Scooter]) -> str:
    """Rendert die Scooter-Liste als HTML-Seite; WARTUNG-Zeilen werden hervorgehoben.

    Reine Funktion, keine I/O.
    """
    zeilen = "\n".join(_zeile(s) for s in scooters)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>CityRide Dashboard</title>
<style>
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #ccc; padding: 4px 8px; }}
tr.wartung {{ background-color: #fdd; }}
</style>
</head>
<body>
<h1>Scooter-Uebersicht</h1>
<table>
<tr><th>ID</th><th>Akku</th><th>Status</th></tr>
{zeilen}
</table>
</body>
</html>
"""


def _zeile(scooter: Scooter) -> str:
    klasse = ' class="wartung"' if scooter.status == WARTUNG else ""
    return (
        f"<tr{klasse}><td>{escape(scooter.id)}</td>"
        f"<td>{scooter.akku}</td>"
        f"<td>{escape(scooter.status)}</td></tr>"
    )
