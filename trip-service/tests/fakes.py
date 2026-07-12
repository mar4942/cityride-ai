from dataclasses import dataclass, field

from trip_service.ports import AbrechnenErgebnis, WalletUnterdeckungError


@dataclass
class FakeFleetPort:
    verfuegbar: dict[str, bool] = field(default_factory=dict)
    angefragt: list[str] = field(default_factory=list)

    def ist_verfuegbar(self, scooter_id: str) -> bool:
        self.angefragt.append(scooter_id)
        return self.verfuegbar.get(scooter_id, False)


@dataclass
class FakePricingPort:
    betrag: int = 0
    wallet_saldo: int = 0
    wallet_unterdeckt: bool = False
    aufrufe: list[dict] = field(default_factory=list)

    def abrechnen(
        self, fahrt_id: str, minuten: int, zone: str, geofence_ok: bool
    ) -> AbrechnenErgebnis:
        self.aufrufe.append(
            {
                "fahrt_id": fahrt_id,
                "minuten": minuten,
                "zone": zone,
                "geofence_ok": geofence_ok,
            }
        )
        if self.wallet_unterdeckt:
            raise WalletUnterdeckungError(fahrt_id)
        return AbrechnenErgebnis(betrag=self.betrag, wallet_saldo=self.wallet_saldo)
