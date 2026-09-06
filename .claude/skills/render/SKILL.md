---
name: render
description: Rendert das freigegebene Storyboard in fünf Format-Varianten (UGC, Cinematic, Reaction, Mirror-Hook, Split-Screen) als 9:16-Clips, wahlweise über den Higgsfield-MCP oder über fal.ai (Seedance 2.0). Zeigt vorher den Preis und wartet auf das Wort freigeben. Für Varianten aus einem eigenen Quellclip lädt er stattdessen den Ad-Multiplier-Workflow.
---

# /render --marke <marke> [--provider higgsfield|fal] [--formate ugc,cinematic,reaction,mirror,split] [--quelle <clip>]

## Voraussetzung

`runs/<id>/rebuild.md` liegt vor und der Operator hat es mit dem Wort `freigeben` bestätigt. Steht das Wort nicht im Chat, stoppen und darauf hinweisen.

## Route A · Storyboard rendern (Standard)

1. **Modell prüfen.** `models_explore action=get model_id=seedance_2_0`. Dauer, Auflösungen und Referenz-Rollen aus der Antwort übernehmen, nicht aus dem Gedächtnis. Wenn das Modell fehlt oder umbenannt ist, `models_explore action=recommend` mit „9:16 product ad with product and character reference images, audio" und das Ergebnis dem Operator nennen, bevor es weitergeht.
2. **Referenzen.** Produktbild-URL aus `brand/<marke>/assets.md` mit `media_import_url` importieren, lokale Datei mit `media_upload`. Die zurückgegebene Media-ID merken. Charakter: Element-ID aus `assets.md`, sonst Beschreibung aus `aesthetic_core.md` in den Prompt.
3. **Fünf Prompts** aus `prompts/formats.md` bauen. Jeder Rahmen um das Storyboard, jeder Prompt endet mit dem Safe-Zone-Satz. Prompts nach `runs/<id>/prompts.md` schreiben, damit sie nachvollziehbar sind.
4. **Preis.** Für jedes Format `generate_video` mit `get_cost: true` aufrufen. Summe in `runs/<id>/cost.md` schreiben und dem Operator zeigen: „5 Formate, <Summe> Credits. freigeben?" Warten.
5. **Rendern.** Nach dem zweiten `freigeben`: `generate_video_batch` mit fünf Anfragen, `index` 1 bis 5 in der Reihenfolge UGC, Cinematic, Reaction, Mirror-Hook, Split-Screen. Parameter: `model: "seedance_2_0"`, `aspect_ratio: "9:16"`, `duration` aus dem Storyboard (Summe der Shot-Dauern, innerhalb der Modellgrenzen), `resolution: "720p"` für die Sichtung, `generate_audio: true`, `medias` mit der Produkt-Media-ID als `image_references`. Die Job-IDs sofort nach `runs/<id>/render.json` schreiben.
6. **Warten.** `jobs_wait` mit allen fünf Jobs und `timeout_seconds: 15`. Solange `all_terminal` falsch ist, nach `poll_after_seconds` erneut aufrufen. Wenn der Operator „status" schreibt, `jobs_wait` mit `timeout_seconds: 0` und den Stand nennen.
7. **Zeigen.** Ein einziger Aufruf `show_generation_by_ids` mit allen fünf. Ergebnis-URLs in `render.json` ergänzen.
8. **Fehler.** Ein Job mit Status failed: genau einmal mit demselben Prompt neu einreichen. Scheitert er wieder, das Format als ausgefallen melden und mit den anderen weitermachen. Nie einen laufenden Job neu einreichen.
9. Wenn Remote Control verbunden ist: Push „Render fertig, <n> von 5 Clips. Weiter mit /label."

## Route C · fal.ai statt Higgsfield (`--provider fal`)

Gleiche Prompts, anderes Modell. Sinnvoll, wenn kein Higgsfield-Guthaben da ist oder der Operator ein bestimmtes Modell will. Der Beispiel-Lauf in `examples/stur-run/` ist so entstanden.

1. `FAL_KEY` in `.env` (fal.ai/dashboard/keys). Guthaben prüfen: `curl -H "Authorization: Key $FAL_KEY" https://rest.alpha.fal.ai/billing/user_balance`.
2. Die fünf Prompts wie in Route A bauen, aber als `runs/<id>/prompts.json`: Liste von `{name, endpoint, input}` mit `endpoint: "bytedance/seedance-2.0/reference-to-video"` und `input: {prompt, image_urls: [<Produktbild-URL>], duration, resolution: "720p", aspect_ratio: "9:16", generate_audio: true}`. Das Produktbild wird im Prompt als `@Image1` referenziert.
3. **Preis.** fal hat keine Kostenabfrage. Preis von der Modellseite nehmen (Stand 06.09.2026: 0,3024 $ pro Sekunde, 720p Standard) und als `cost.md` mit Summe zeigen. Auf `freigeben` warten.
4. `FAL_KEY=… python3 scripts/render-fal.py runs/<id>/prompts.json runs/<id>/raw`. Das Skript reicht alle Jobs parallel ein, pollt, lädt die MP4s und schreibt `render.json` mit Ergebnis-URLs. Die fal-URLs sind öffentlich, `/label` kann sie direkt als `video_url` verwenden.
5. Weiter wie Route A ab Schritt 8.

## Route B · eigener Quellclip (`--quelle`)

Wenn der Operator einen eigenen Clip zwischen 4 und 30 Sekunden hat und daraus Varianten will (andere Person, anderes Produkt, anderer Hintergrund): **nicht** Route A. Stattdessen `get_workflow_instructions workflow="ad-multiplier"` laden und dem Workflow folgen. Er verlangt Analyse, Referenz-Mapping und Freigabe je Person, und rendert stumm mit anschließender Tonrückführung. Ergebnis ebenfalls nach `runs/<id>/render.json`, Icon später `ai-modified-*`, weil echtes Material bearbeitet wurde.

## Was der Skill nicht tut

- Keine Auflösung über 720p ohne ausdrücklichen Wunsch. Der Preis steigt, die Sichtung braucht es nicht.
- Kein `use_unlim` aus eigener Initiative. Nur wenn der Operator ausdrücklich seine Gratis-Generierungen einsetzen will.
- Kein Upload zu Meta.
