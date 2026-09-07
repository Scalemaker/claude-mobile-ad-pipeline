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

1. **Icon wählen.** Vollständig generierte Clips: `ai-generated-black`, auf dunklem Bild `ai-generated-white`. Bearbeitetes echtes Material (Ad-Multiplier): `ai-modified-*`. Wenn unklar: `list_icons` aufrufen und dem Operator die Wahl zeigen.
2. **Position.** Für 9:16: `x: 14`, `y: 20`, `size: 12`. Das legt das Icon links oben in die Reels-Safe-Zone (oberer Rand der Zone bei 14 % Höhe, linker Rand bei 6 % Breite, gemessen an Metas Safe-Zone-Vorlage). Nicht `position: "bottom-right"`, dort liegt bei Reels die Aktionsleiste über dem Bild.
3. **Größe prüfen, bevor du kennzeichnest.** Der MCP nimmt keine beliebig großen Dateien und gibt die gekennzeichnete Datei nur bis rund 4 MB zurück. Gemessen am 06.09.2026 an fünf Seedance-Clips: 3,9 MB und 3,4 MB liefen durch, 5,0 MB kam als `413 FUNCTION_PAYLOAD_TOO_LARGE` zurück, und ein Clip mit 2,2 MB Eingang lieferte 4,6 MB Ausgang, der nicht mehr zurückkam. Also:

   ```bash
   # kleiner rechnen, bis die Datei klar unter 3,5 MB liegt
   ffmpeg -y -i raw/<format>.mp4 -c:v libx264 -preset slow -crf 24 -c:a aac -b:a 128k -movflags +faststart raw/<format>-small.mp4
   # bei bewegten Handkamera-Clips reicht crf allein oft nicht, dann zusätzlich skalieren:
   ffmpeg -y -i raw/<format>.mp4 -vf scale=540:-1 -c:v libx264 -preset slow -crf 26 -c:a aac -b:a 96k -movflags +faststart raw/<format>-small.mp4
   ```

   Danach eine öffentliche URL besorgen, denn `label_video` liest per URL: `FAL_KEY=… python3 scripts/fal-upload.py raw/<format>-small.mp4` gibt sie aus. Ergebnis-URLs aus dem Render sind bereits öffentlich und können direkt verwendet werden, solange sie klein genug sind.
4. **Kennzeichnen.** Je Clip `label_video` mit `video_url`, `icon`, `x`, `y`, `size`, `embed_metadata: true`. Mit `--register` zusätzlich `register_entry: true`, dann erscheint der Clip im Kennzeichnungs-Register des Accounts als Nachweis.
5. **Speichern.** Die zurückgegebene Datei nach `runs/<id>/final/<format>-labeled.mp4`.
6. **Prüfen.** Für jede Datei `scripts/contact-sheet.sh runs/<id>/final/<format>-labeled.mp4`. Das Skript zieht drei Frames, zeichnet die Reels-Safe-Zone als L ein und meldet, ob `DigitalSourceType` im File steht. Kontaktblatt ansehen: Icon innerhalb der grünen Zone? Hook-Overlay nicht unter der roten Leiste?
7. **Melden.** Liste der Clips mit Icon, Position und Markierungsstatus. Wenn Remote Control verbunden ist: Push „Clips gekennzeichnet in runs/<id>/final".

## Ausgabe

```
runs/<id>/final/
├── ugc-labeled.mp4          + ugc-sheet.jpg
├── cinematic-labeled.mp4    + …
├── reaction-labeled.mp4
├── mirror-labeled.mp4
└── split-labeled.mp4
```

## Was der Skill nicht tut

- Er sagt nicht „rechtssicher" oder „konform". Er setzt Icon und Markierung.
- Er entfernt keine Markierung und überschreibt keine gekennzeichnete Datei.
- Er kennzeichnet nicht nach dem Schnitt. Reihenfolge: schneiden, dann kennzeichnen, dann hochladen. Ein Export nach dem Kennzeichnen wirft die XMP-Ebene wieder raus.
