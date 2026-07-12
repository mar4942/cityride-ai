from pydantic import BaseModel


class AbrechnenRequest(BaseModel):
    fahrt_id: str
    minuten: int
    zone: str
    geofence_ok: bool


class AbrechnenResponse(BaseModel):
    betrag: int
    wallet_saldo: int
