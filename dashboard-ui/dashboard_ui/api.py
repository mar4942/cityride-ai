import os

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse

from dashboard_ui.adapters.fleet_http import HttpFleetPort
from dashboard_ui.ports import FleetPort
from dashboard_ui.render import render_dashboard

FLEET_SERVICE_URL = os.environ.get("FLEET_SERVICE_URL", "http://localhost:8001")

app = FastAPI()

_fleet_port: FleetPort = HttpFleetPort(base_url=FLEET_SERVICE_URL)


def get_fleet_port() -> FleetPort:
    return _fleet_port


@app.get("/", response_class=HTMLResponse)
def dashboard(fleet: FleetPort = Depends(get_fleet_port)) -> str:
    return render_dashboard(fleet.list_scooters())
