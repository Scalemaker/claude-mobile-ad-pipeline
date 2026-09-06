---
name: label
description: Setzt auf jeden gerenderten Clip das offizielle EU-Icon und die maschinenlesbare XMP/IPTC-Markierung über den KI-Kennzeichnung-MCP, platziert innerhalb der Reels-Safe-Zone. Danach Kontaktblatt pro Clip und Nachweis der Markierung im File. Verwenden nach /render, vor jeder Weitergabe eines Clips.
---

# /label [--icon ai-generated-black|ai-generated-white|ai-modified-black|ai-modified-white] [--register]

## Voraussetzung

`runs/<id>/render.json` mit mindestens einer Ergebnis-URL.

## Warum das ein Pipeline-Schritt ist

Seit dem 2. August 2026 gilt Art. 50 EU AI Act. Er kennt zwei Rollen mit zwei Pflichten: Anbieter eines KI-Systems markieren Ausgaben maschinenlesbar (Abs. 2), Betreiber legen bei Deepfakes sichtbar offen (Abs. 4). Welche Rolle der Operator hat und ob ein bestimmter Clip darunterfällt, beurteilt dieser Skill nicht. Er sorgt dafür, dass beides technisch gesetzt ist, bevor jemand den Clip weitergibt: das Icon im Bild, die Markierung im File. Die Entscheidung, ob das im Einzelfall reicht, bleibt beim Operator.

## Ablauf

1. **Icon wählen.** Vollständig generierte Clips (Route A): `ai-generated-black`, auf dunklem Bild `ai-generated-white`. Bearbeitetes echtes Material (Ad-Multiplier): `ai-modified-*`. Wenn unklar: `list_icons` aufrufen und dem Operator die Wahl zeigen.
2. **Position.** Für 9:16: `x: 14`, `y: 20`, `size: 12`. Das legt das Icon links oben in die Reels-Safe-Zone (oberer Rand der Zone bei 14 % Höhe, linker Rand bei 6 % Breite, gemessen an Metas Safe-Zone-Vorlage). Nicht `position: "bottom-right"`, dort liegt bei Reels die Aktionsleiste über dem Bild.
3. **Kennzeichnen.** Je Clip `label_video` mit `video_url` (die Higgsfield-Ergebnis-URL), `icon`, `x`, `y`, `size`, `embed_metadata: true`. Mit `--register` zusätzlich `register_entry: true`, dann erscheint der Clip im Kennzeichnungs-Register des Accounts als Nachweis.
4. **Speichern.** Die zurückgegebene Datei nach `runs/<id>/final/<format>-labeled.mp4`.
5. **Prüfen.** Für jede Datei `scripts/contact-sheet.sh runs/<id>/final/<format>-labeled.mp4`. Das Skript zieht drei Frames, zeichnet die Reels-Safe-Zone als L ein und meldet, ob `DigitalSourceType` im File steht. Kontaktblatt ansehen: Icon innerhalb der grünen Zone? Hook-Overlay nicht unter der roten Leiste?
6. **Melden.** Liste der fünf Clips mit Icon, Position und Markierungsstatus. Wenn Remote Control verbunden ist: Push „5 Clips gekennzeichnet in runs/<id>/final".

## Ausgabe

```
runs/<id>/final/
├── ugc-labeled.mp4          + ugc-labeled-sheet.jpg
├── cinematic-labeled.mp4    + …
├── reaction-labeled.mp4
├── mirror-labeled.mp4
└── split-labeled.mp4
```

## Was der Skill nicht tut

- Er sagt nicht „rechtssicher" oder „konform". Er setzt Icon und Markierung.
- Er entfernt keine Markierung und überschreibt keine gekennzeichnete Datei.
