# CityRide — Vibe & AI Coding

Dasselbe Projekt (E-Scooter-Sharing) in drei Reifegraden.

## Teil A — UI (nur Oberfläche)
Ordner: `ai/a-ui/` — vier Screens mit v0.dev, iterativ erzeugt.
Screenshots + Prompts im Ordner.

## Teil B — Vibe-App (lauffähig)
Ordner: `ai/b-vibe/` — mit bolt.new gebaut, Live-Link in `live-link.md`.
Datenhaltung bewusst lokal (In-Memory), "Vibe-Qualität", kein Backend.

## Teil C — modulare, verteilte App (Schwerpunkt)
Module: `pricing-service`, `geofence-service`, `fleet-service`,
`trip-service`, `dashboard-ui`, `mock-scooter`.
Spec-getrieben (`specs/`), reine Domänenlogik + Ports/Adapters, Tests je Modul.
Prompts und Screenshots in `ai/c-app/`.

## Werkzeuge
v0.dev, bolt.new, Claude Code, Cline — vier Werkzeuge, zwei Arten:
- CLI-Agent: Claude Code (fünf Services)
- IDE-Plugin: Cline (mock-scooter)