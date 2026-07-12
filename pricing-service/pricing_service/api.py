from fastapi import FastAPI, HTTPException

from pricing_service.models import AbrechnenRequest, AbrechnenResponse
from pricing_service.pricing import berechne_betrag
from pricing_service.wallet import Wallet, WalletUnterdeckungError, belasten

STARTGUTHABEN_CENT = 1000

app = FastAPI()
_wallets: dict[str, Wallet] = {}


@app.post("/abrechnen", response_model=AbrechnenResponse)
def abrechnen(req: AbrechnenRequest) -> AbrechnenResponse:
    betrag = berechne_betrag(req.minuten, req.zone, req.geofence_ok)
    wallet = _wallets.setdefault(req.fahrt_id, Wallet(saldo_cent=STARTGUTHABEN_CENT))

    try:
        neues_wallet = belasten(wallet, betrag)
    except WalletUnterdeckungError as exc:
        raise HTTPException(status_code=402, detail=str(exc)) from exc

    _wallets[req.fahrt_id] = neues_wallet
    return AbrechnenResponse(betrag=betrag, wallet_saldo=neues_wallet.saldo_cent)
