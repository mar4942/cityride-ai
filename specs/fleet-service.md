# fleet-service
## Zweck
Verwaltet Scooter-Zustaende und Akku (Telematik).
## Öffentliche Schnittstelle
GET /scooter/{id} -> {id, akku, status, position}
POST /scooter/{id}/status {status} -> {id, status}
## Fachregeln
- Zustaende: VERFUEGBAR, RESERVIERT, IN_FAHRT, WARTUNG, LADEN, OFFLINE
- akku < 15 -> status WARTUNG, nicht mehr vermittelbar
## Tests (Akzeptanz)
- Scooter mit akku 10 -> status WARTUNG
- Scooter mit akku 80 -> status VERFUEGBAR