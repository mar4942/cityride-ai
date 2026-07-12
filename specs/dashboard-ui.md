# Prompts – Teil A (UI)

**Tool:** v0.dev
**Ziel:** vier UI-Screens für die CityRide-App, nur Oberfläche, keine Logik.

## Iteration 1 – Kartenansicht
Prompt:
"Design a mobile screen for an e-scooter sharing app called CityRide.
A map placeholder at the top, below it a scrollable list of nearby scooters.
Each item shows scooter ID, distance in meters, battery % with a color-coded
icon (green >50%, orange 15–50%, red <15%), and a primary button 'Entsperren'.
Clean modern light theme, mobile-first. UI only, no logic."
Ergebnis: 01-karte.png

## Iteration 2 – Fahrt aktiv
Prompt:
"Add an 'Fahrt aktiv' screen: a large live timer (mm:ss), the running fare
in euros below it, the current scooter ID, a map placeholder, and a
prominent red button 'Fahrt beenden' at the bottom. Same style as before."
Ergebnis: 02-fahrt-aktiv.png

## Iteration 3 – Fahrtende / Rechnung
Prompt:
"Add a receipt screen listing Freischaltgebühr 1,00 €, Minutenpreis 0,20 €/min,
optional Innenstadt-Zuschlag 0,50 €, optional Strafgebühr 5,00 €, and a bold total.
Add a zone status badge and a 'Fertig' button."
Ergebnis: 03-rechnung.png

## Iteration 4 – Empty State
Prompt:
"Add an empty-state screen: friendly illustration, headline
'Kein Scooter in der Nähe', short subtext, and a 'Karte aktualisieren' button."
Ergebnis: 04-empty-state.png

## Kurzfazit 
Ich habe die vier Screens mit v0.dev in mehreren Iterationen erzeugt. Jede
Iteration hat auf der vorigen aufgebaut ("Add ...", "same style"), sodass ein
einheitlicher Look entstand. Die Fachregeln (15%-Akkugrenze, Tarifwerte,
Geofence-Strafgebühr) habe ich bewusst direkt in die Prompts eingebaut, damit
das UI fachlich zu CityRide passt.