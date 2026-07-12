from pydantic import BaseModel


class StartRequest(BaseModel):
    scooter_id: str
    fahrer_id: str


class StartResponse(BaseModel):
    fahrt_id: str
    status: str


class BeendenRequest(BaseModel):
    zone: str
    geofence_ok: bool


class BeendenResponse(BaseModel):
    status: str
    betrag: int
