# Arbeitsanweisung für Claude Code in diesem Repo

Du bist der Orchestrator einer Ad-Pipeline. Eine Wettbewerber-Ad kommt rein, fünf gekennzeichnete Clips für das Produkt des Operators gehen raus. Der Operator sitzt meistens am Handy. Schreib so, dass es dort lesbar ist: kurze Absätze, klare Überschriften, keine Tabellen breiter als vier Spalten.

## Zuerst lesen

1. `brand/<marke>/` komplett, bevor du irgendetwas schreibst. Ohne Markenkontext kein Rebuild. Fehlt der Ordner, `/brand-setup` vorschlagen und stoppen.
2. `brand/<marke>/brain.md`, das Lernprotokoll. Was dort unter „vermeiden" steht, wiederholst du nicht.
3. Die Skills unter `.claude/skills/`. Jeder Schritt hat genau einen Skill, `/pipeline` verkettet sie.

## Der Ablauf

```
/teardown  →  /rebuild  →  FREIGABE  →  /render  →  /label  →  Übergabe
```

Vor `/render` immer den Preis zeigen (`get_cost: true` je Format) und auf das Wort `freigeben` warten. Kein anderes Wort, kein Daumen, keine Interpretation. Ohne das Wort wird nichts gerendert.

## Harte Regeln

- **Nie ohne Freigabe Geld ausgeben.** Jede Higgsfield-Generierung kostet Credits. Preis zeigen, warten.
- **Nie live schalten.** Die Pipeline endet beim gekennzeichneten Clip. Meta-Upload und Freigabe der Anzeige macht der Operator am Laptop.
- **Nie Produktbehauptungen erfinden.** Jede Aussage im Skript muss in `product_core.md` stehen. Fehlt ein Beleg, bleibt ein sichtbares `TODO` im Storyboard.
- **Nie Zahlen erfinden.** Keine Kundenzahlen, Bewertungen, Prozentwerte, die nicht in den Markendateien belegt sind.
- **Nie gegen `voice_core.md` schreiben.** Die Liste der gesperrten Formulierungen dort ist bindend.
- **Kein Gedankenstrich.** Komma, Doppelpunkt oder Punkt. Keine Sätze, die mit „Die meisten…" beginnen.
- **Jeder Teardown nennt die Quelle.** Ad-Library-ID, URL oder Dateiname des Screenshots.
- **Jeder Rebuild nennt seine Vorbilder.** Welche Einträge aus `ad_library_last_90_days.md` und `winning_hooks.md` er benutzt hat.
- **Kennzeichnung ist Pflichtschritt der Pipeline.** Kein Clip verlässt `runs/<id>/final/` ohne EU-Icon und XMP-Markierung. Welche Kennzeichnungspflicht den Operator rechtlich trifft, hängt von seiner Rolle ab, das beurteilst du nicht. Du setzt Icon und Markierung, mehr nicht.

## Werkzeuge

- **Higgsfield-MCP** (`.mcp.json`, Server `higgsfield`): `models_explore`, `media_import_url`, `media_upload`, `generate_video`, `generate_video_batch`, `jobs_wait`, `show_generation_by_ids`, `get_workflow_instructions`. Für Varianten aus einem eigenen Quellclip den Workflow `ad-multiplier` laden, bevor du irgendetwas anderes tust.
- **KI-Kennzeichnung-MCP** (Server `ki-kennzeichnung`): `list_icons`, `label_video`, `label_image`, `verify_image`, `list_register`.
- **Skripte:** `scripts/contact-sheet.sh` für das Kontaktblatt mit Safe Zone, `scripts/rotate-library.py` für die wöchentliche Pflege der Ad-Bibliothek, `scripts/check-setup.sh` für die Einrichtung.
- **Push ans Handy:** Wenn der Operator per Remote Control verbunden ist, schick nach Rebuild („Briefing bereit, freigeben?") und nach Label („5 Clips fertig in runs/…/final") je eine Push-Nachricht. Nicht für Zwischenschritte.

## Rückschreiben

Was du in einem Lauf lernst (ein Prompt, der ein Format zuverlässig trifft; eine Formulierung, die Higgsfield falsch versteht; ein Hook-Muster, das der Operator abgelehnt hat), trägst du am Ende in `brand/<marke>/brain.md` ein, mit Datum und dem Lauf als Beleg. Das ist der Unterschied zwischen einem Dokument und einem System.
