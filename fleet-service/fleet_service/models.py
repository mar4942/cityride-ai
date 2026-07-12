from pydantic import BaseModel


class Position(BaseModel):
    lat: float
    lng: float


class ScooterResponse(BaseModel):
    id: str
    akku: int
    status: str
    position: Position


class StatusRequest(BaseModel):
    status: str


class StatusResponse(BaseModel):
    id: str
    status: str
