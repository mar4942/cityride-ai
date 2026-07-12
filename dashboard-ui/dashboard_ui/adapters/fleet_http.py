import httpx

from dashboard_ui.models import Scooter


class HttpFleetPort:
    """FleetPort-Implementierung, die fleet-service ueber HTTP befragt."""

    def __init__(self, base_url: str):
        self._base_url = base_url

    def list_scooters(self) -> list[Scooter]:
        response = httpx.get(f"{self._base_url}/scooters")
        response.raise_for_status()
        return [
            Scooter(id=s["id"], akku=s["akku"], status=s["status"]) for s in response.json()
        ]
