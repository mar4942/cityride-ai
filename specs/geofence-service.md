# geofence-service
## Zweck
Prueft, ob ein Punkt in einer erlaubten Zone liegt.
## Öffentliche Schnittstelle
POST /pruefen {lat, lng} -> {in_zone: bool, zone: string}
## Fachregeln
- erlaubte Zone = einfaches Rechteck (min/max lat, min/max lng)
- Punkt ausserhalb -> in_zone=false
## Tests (Akzeptanz)
- Punkt in der Zone -> in_zone=true
- Punkt ausserhalb -> in_zone=false