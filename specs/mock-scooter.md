# mock-scooter
## Zweck
Steuerbares Test-Target, das einen Scooter simuliert.
## Öffentliche Schnittstelle
POST /set-akku {level}
POST /lock  /  POST /unlock
POST /set-position {lat, lng}
## Verhalten
- jede Zustandsaenderung wird als Nachricht auf "scooter/<id>/state" veröffentlicht (MQTT)
- einfache REST- oder CLI-Bedienung zum manuellen Testen
## Wird gebaut mit: Cline (IDE-Plugin) — nachweis der zweiten Werkzeug-Art