# Prompts – Teil C (modulare, verteilte App)

**Werkzeug-Art 1 (CLI-Agent):** Claude Code — für pricing-, geofence-, fleet-,
trip-service und dashboard-ui.
**Werkzeug-Art 2 (IDE-Plugin):** Cline (in VS Code, Modell deepseek-v4-flash)
— für mock-scooter.

**Vorgehen (bei jedem Modul gleich):** erst Spec (specs/*.md), dann Plan zeigen
lassen, prüfen, umsetzen lassen, Tests grün, committen (Specification-Driven,
"Planning vor Write").


## pricing-service (Claude Code)
Planning-Prompt:
"Read specs/pricing-service.md. Before writing any code, produce a step-by-step
implementation plan: which files you'll create under a folder 'pricing-service/',
the public interface, and which pytest tests you'll write. Use Python + FastAPI,
keep the pricing/wallet logic pure (no I/O). Do NOT write code yet — show me the
plan first."

Antwort auf Rückfrage (Wallet-Guthaben):
"Per-fahrt_id, auto-seeded default balance."
"Yes, this matches what I want. Please implement it now, then run the tests and
show me the results."

Eigene Entscheidung: Die Spec definierte kein Wallet-Aufladen. Gewählt: pro
fahrt_id automatisch angelegtes Startguthaben, weil das die dokumentierte
Schnittstelle nicht erweitert und den 402-Fall (Unterdeckung) testbar macht.
Bei Unterdeckung 402 + keine Abbuchung (Immutability).


## geofence-service (Claude Code)
Planning-Prompt:
"Now read specs/geofence-service.md. Show me the implementation plan first
(files under 'geofence-service/', public interface, pytest tests).
Python + FastAPI, logic pure (no I/O). No code yet — plan first."

Antwort auf Rückfrage (Zonen-Definition):
"Yes, this structure works. Use placeholder rectangle bounds and the names
STADTGEBIET / AUSSERHALB. Treat boundary points as inside (inclusive).
Now implement it and run the tests."

Eigene Entscheidung: Keine konkreten Koordinaten in der Spec → Platzhalter-
Rechteck mit inklusiven Grenzen, da die genaue Geometrie für die Logik nicht
entscheidend ist; wichtig ist die Punkt-in-Zone-Prüfung.


## fleet-service (Claude Code)
Planning-Prompt:
"Now read specs/fleet-service.md. Show me the implementation plan first
(files under 'fleet-service/', public interface, pytest tests).
Python + FastAPI, logic pure (no I/O). No code yet — plan first."

Antwort auf Rückfragen (Position / unbekannte IDs):
"Keep position as a {lat, lng} object. GET should return 404 for unknown ids
(don't auto-provision). This all matches — implement it and run the tests."

Eigene Entscheidung: GET berechnet den Status immer neu aus dem Akkustand,
damit die 15%-Wartungsregel nicht durch einen veralteten gespeicherten Status
umgangen werden kann. Unbekannte IDs → 404 statt automatisch anlegen.


## trip-service (Claude Code)
Planning-Prompt:
"Now read specs/trip-service.md. Show me the implementation plan first
(files under 'trip-service/', public interface, pytest tests).
Python + FastAPI, logic pure (no I/O). No code yet — plan first."

Design-Vorgabe (Anbindung an fleet/pricing):
"Use ports/interfaces for the fleet and pricing dependencies (dependency
inversion), so the trip domain logic stays pure and testable. In the tests,
inject fake/stub implementations instead of calling real services over HTTP."

Umsetzen:
"This matches. Implement it and run the tests."

Eigene Entscheidungen:
- trip-service hängt über Ports (Interfaces) an fleet und pricing, nicht an
  konkreten HTTP-Clients → Kern bleibt rein und testbar (Stubs in den Tests).
- Ein 402 von pricing (Wallet unterdeckt) wird durchgereicht.
- 409 (Conflict) statt 400, wenn eine Fahrt schon beendet ist, weil es ein
  Zustandskonflikt ist, kein Eingabefehler.


## dashboard-ui (Claude Code)
Planning-Prompt:
"Now read specs/dashboard-ui.md. Show me the implementation plan first
(files under 'dashboard-ui/', public interface). Keep it deliberately simple —
one page that lists scooters with battery and status and highlights those in
WARTUNG. No code yet — plan first."

Antwort auf Rückfrage (Datenquelle für die Liste):
"Add GET /scooters to fleet-service."
"This matches. Implement it and run the tests."

Eigene Entscheidung: Für die Liste einen GET /scooters-Endpoint im fleet-service
ergänzt, statt IDs im Dashboard fest zu verdrahten — der fleet-service ist für
die Scooter-Daten zuständig (Single Responsibility). Dashboard rendert
serverseitig eine einfache HTML-Seite ohne JS-Framework; Hervorhebungs-Logik in
einer reinen render-Funktion (testbar ohne Server).


## mock-scooter (Cline / IDE-Plugin)
Prompt:
"Read specs/mock-scooter.md. Create a 'mock-scooter' module in Python: a small
controllable test target that simulates an e-scooter. Add endpoints to set the
battery level, lock/unlock, and set the position (lat/lng), and publish each
change as an MQTT message on topic 'scooter/<id>/state'. Add a simple way to
trigger changes manually for testing (REST or CLI). Build it step by step and
explain each file as you go."

Grund für separates Werkzeug: Nachweis der zweiten Werkzeug-Art (IDE-Plugin).
Ergebnis: Flask-REST-API + CLI + MQTT-Publisher; Service läuft auf Port 5000,
MQTT verbindet auf localhost:1883.
Hinweis: Clines automatischer End-to-End-Check schlug wegen eines
Anführungszeichen-Fehlers in seinem inline python -c-Befehl fehl — nicht wegen
des Moduls. Verifiziert durch direkten Start via python run.py.


## Kurzfazit
Jedes Modul entstand spec-getrieben: erst Spezifikation, dann Plan prüfen,
umsetzen, Tests grün, committen. Zwei Werkzeug-Arten: Claude Code (CLI) für
fünf Services, Cline (IDE-Plugin) für mock-scooter. Durchgängiges Muster:
reine Domänenlogik + Ports/Adapters, damit der Kern ohne Netz/DB testbar ist.