from fastapi import FastAPI

from geofence_service.geofence import pruefe_punkt
from geofence_service.models import PruefenRequest, PruefenResponse

app = FastAPI()


@app.post("/pruefen", response_model=PruefenResponse)
def pruefen(req: PruefenRequest) -> PruefenResponse:
    in_zone, zone = pruefe_punkt(req.lat, req.lng)
    return PruefenResponse(in_zone=in_zone, zone=zone)
