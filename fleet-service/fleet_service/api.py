from fastapi import FastAPI, HTTPException

from fleet_service.fleet import (
    VERFUEGBAR,
    WARTUNG,
    Scooter,
    StatusUngueltigError,
    berechne_status,
    setze_status,
)
from fleet_service.models import Position, ScooterResponse, StatusRequest, StatusResponse

app = FastAPI()

_scooters: dict[str, Scooter] = {
    "scooter-1": Scooter(id="scooter-1", akku=80, status=VERFUEGBAR, position=(48.20, 11.55)),
    "scooter-2": Scooter(id="scooter-2", akku=10, status=WARTUNG, position=(48.15, 11.60)),
}


def _zu_response(scooter: Scooter) -> ScooterResponse:
    status = berechne_status(scooter.akku, scooter.status)
    lat, lng = scooter.position
    return ScooterResponse(
        id=scooter.id,
        akku=scooter.akku,
        status=status,
        position=Position(lat=lat, lng=lng),
    )


@app.get("/scooter/{id}", response_model=ScooterResponse)
def get_scooter(id: str) -> ScooterResponse:
    scooter = _scooters.get(id)
    if scooter is None:
        raise HTTPException(status_code=404, detail="Scooter nicht gefunden")
    return _zu_response(scooter)


@app.post("/scooter/{id}/status", response_model=StatusResponse)
def setze_scooter_status(id: str, req: StatusRequest) -> StatusResponse:
    scooter = _scooters.get(id)
    if scooter is None:
        raise HTTPException(status_code=404, detail="Scooter nicht gefunden")

    try:
        neuer_scooter = setze_status(scooter, req.status)
    except StatusUngueltigError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    _scooters[id] = neuer_scooter
    return StatusResponse(id=neuer_scooter.id, status=neuer_scooter.status)
