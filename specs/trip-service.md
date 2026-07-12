# trip-service
## Zweck
Steuert den Lebenszyklus einer Fahrt (Zustandsautomat).
## Öffentliche Schnittstelle
POST /fahrt/start {scooter_id, fahrer_id} -> {fahrt_id, status}
POST /fahrt/{fahrt_id}/beenden {zone, geofence_ok} -> {status, betrag}
## Fachregeln
- Zustaende: GESTARTET -> BEENDET
- start nur, wenn Scooter verfuegbar (fleet-service fragt)
- beenden ruft pricing-service /abrechnen auf
## Tests (Akzeptanz)
- start liefert fahrt_id und status GESTARTET
- beenden setzt status BEENDET und liefert betrag