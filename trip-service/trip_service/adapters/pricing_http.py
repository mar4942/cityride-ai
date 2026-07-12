import httpx

from trip_service.ports import AbrechnenErgebnis, WalletUnterdeckungError


class HttpPricingPort:
    """PricingPort-Implementierung, die pricing-service ueber HTTP befragt."""

    def __init__(self, base_url: str):
        self._base_url = base_url

    def abrechnen(
        self, fahrt_id: str, minuten: int, zone: str, geofence_ok: bool
    ) -> AbrechnenErgebnis:
        response = httpx.post(
            f"{self._base_url}/abrechnen",
            json={
                "fahrt_id": fahrt_id,
                "minuten": minuten,
                "zone": zone,
                "geofence_ok": geofence_ok,
            },
        )
        if response.status_code == 402:
            raise WalletUnterdeckungError(fahrt_id)
        response.raise_for_status()
        body = response.json()
        return AbrechnenErgebnis(betrag=body["betrag"], wallet_saldo=body["wallet_saldo"])
