# pricing-service
## Zweck
Berechnet den Fahrtpreis und belastet das Wallet.
## Öffentliche Schnittstelle
POST /abrechnen {fahrt_id, minuten, zone, geofence_ok} -> {betrag, wallet_saldo}
## Fachregeln (alles in Cent)
- Betrag = 100 (Freischaltung) + 20 * minuten
- zone == "INNENSTADT": + 50 Zonenzuschlag
- geofence_ok == false: + 500 Strafgebühr
- Wallet-Unterdeckung: HTTP 402, Fahrt sperren
## Tests (Akzeptanz)
- 10 min, STANDARD, geofence_ok=true  -> 300
- 10 min, INNENSTADT, geofence_ok=true -> 350
- 10 min, STANDARD, geofence_ok=false -> 800
- Wallet-Saldo < Betrag -> 402 abgelehnt