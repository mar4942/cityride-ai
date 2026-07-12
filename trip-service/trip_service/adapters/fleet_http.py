import httpx

VERFUEGBAR = "VERFUEGBAR"


class HttpFleetPort:
    """FleetPort-Implementierung, die fleet-service ueber HTTP befragt."""

    def __init__(self, base_url: str):
        self._base_url = base_url

    def ist_verfuegbar(self, scooter_id: str) -> bool:
        response = httpx.get(f"{self._base_url}/scooter/{scooter_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return response.json()["status"] == VERFUEGBAR
