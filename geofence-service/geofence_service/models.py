from pydantic import BaseModel


class PruefenRequest(BaseModel):
    lat: float
    lng: float


class PruefenResponse(BaseModel):
    in_zone: bool
    zone: str
