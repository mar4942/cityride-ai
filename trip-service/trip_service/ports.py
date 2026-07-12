from dataclasses import dataclass
from typing import Protocol


class WalletUnterdeckungError(Exception):
    def __init__(self, fahrt_id: str):
        self.fahrt_id = fahrt_id
        super().__init__(f"Wallet-Unterdeckung fuer Fahrt: {fahrt_id}")


@dataclass(frozen=True)
class AbrechnenErgebnis:
    betrag: int
    wallet_saldo: int


class FleetPort(Protocol):
    def ist_verfuegbar(self, scooter_id: str) -> bool: ...


class PricingPort(Protocol):
    def abrechnen(
        self, fahrt_id: str, minuten: int, zone: str, geofence_ok: bool
    ) -> AbrechnenErgebnis: ...
