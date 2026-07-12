import os

from fastapi import Depends, FastAPI, HTTPException

from trip_service.adapters.fleet_http import HttpFleetPort
from trip_service.adapters.pricing_http import HttpPricingPort
from trip_service.models import BeendenRequest, BeendenResponse, StartRequest, StartResponse
from trip_service.ports import WalletUnterdeckungError
from trip_service.service import FahrtNichtGefundenError, FahrtService
from trip_service.trip import FahrtBereitsBeendetError, ScooterNichtVerfuegbarError

FLEET_SERVICE_URL = os.environ.get("FLEET_SERVICE_URL", "http://localhost:8001")
PRICING_SERVICE_URL = os.environ.get("PRICING_SERVICE_URL", "http://localhost:8003")

app = FastAPI()

_fahrt_service = FahrtService(
    fleet=HttpFleetPort(base_url=FLEET_SERVICE_URL),
    pricing=HttpPricingPort(base_url=PRICING_SERVICE_URL),
)


def get_fahrt_service() -> FahrtService:
    return _fahrt_service


@app.post("/fahrt/start", response_model=StartResponse)
def start_fahrt(
    req: StartRequest, service: FahrtService = Depends(get_fahrt_service)
) -> StartResponse:
    try:
        fahrt = service.start(req.scooter_id, req.fahrer_id)
    except ScooterNichtVerfuegbarError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return StartResponse(fahrt_id=fahrt.fahrt_id, status=fahrt.status)


@app.post("/fahrt/{fahrt_id}/beenden", response_model=BeendenResponse)
def beenden_fahrt(
    fahrt_id: str,
    req: BeendenRequest,
    service: FahrtService = Depends(get_fahrt_service),
) -> BeendenResponse:
    try:
        fahrt, betrag = service.beenden(fahrt_id, req.zone, req.geofence_ok)
    except FahrtNichtGefundenError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FahrtBereitsBeendetError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except WalletUnterdeckungError as exc:
        raise HTTPException(status_code=402, detail=str(exc)) from exc
    return BeendenResponse(status=fahrt.status, betrag=betrag)
