---
name: rebuild
description: Baut aus einem fertigen Teardown ein Storyboard für das eigene Produkt. Gleiche Mechanik, gleicher emotionaler Bogen, gleicher Belief Shift, neuer Hook, neues Skript, eigener Charakter. Verwenden nach /teardown. Mit --angles entstehen drei Rebuilds entlang Pain, Benefit, Proof statt einem.
---

# /rebuild [--angles] --marke <marke>

## Voraussetzung

`runs/<id>/teardown.md` existiert. Wenn mehrere Läufe offen sind, nach dem Lauf fragen.

## Ablauf

1. Alle Dateien in `brand/<marke>/` lesen. Zuerst `brain.md`: was unter „vermeiden" steht, ist tabu.
2. Prompt aus `prompts/rebuild.md` ausführen. Mit `--angles` die Variante am Ende der Datei, das ergibt drei Storyboards.
3. Jede Produktaussage im Storyboard gegen `product_core.md` „Belegte Aussagen" prüfen. Ohne Beleg: `TODO: Beleg für „…"` direkt in die Zeile.
4. Hook gegen `voice_core.md` „Gesperrt" prüfen. Trifft ein Wort, Hook neu schreiben.
5. Overlays gegen die Safe Zone prüfen: Text im Storyboard nur „oben" oder „Mitte", nie „unten rechts". Der Grund steht in `scripts/contact-sheet.sh`: bei Reels ragt die Aktionsleiste rechts unten in die Safe Zone.
6. Ausgabe nach `runs/<id>/rebuild.md` (bei `--angles`: `rebuild-pain.md`, `rebuild-benefit.md`, `rebuild-proof.md`).
7. Dem Operator zeigen, am Handy lesbar: Hook, dann das Storyboard als Liste (ein Shot pro Absatz), dann die Locks. Abschließen mit: „Briefing bereit. Antworte mit `freigeben`, dann hole ich den Preis für die fünf Formate."

## Was „Knochen behalten" konkret heißt

| Bleibt | Wird neu |
|---|---|
| Hook-Mechanik (z. B. contrarian) | Hook-Zeile |
| Überzeugungsmechanik (z. B. risk-reversal) | Skript, Beweise, Sprache |
| Form des Bogens (wo Peak und Loch liegen) | die Auslöser an diesen Stellen |
| Belief-Shift-Struktur (vorher → nachher) | der konkrete Glaubenssatz des eigenen ICP |

Wenn der Rebuild in der Formulierung noch nach der Quelle klingt, ist er zu nah dran. Test: Würde jemand, der beide Ads hintereinander sieht, „kopiert" sagen? Dann Hook und Sprache noch einmal weiter weg schreiben, Mechanik behalten.

## Rückschreiben

Wenn der Operator den Rebuild ablehnt oder umschreibt, den Grund in `brand/<marke>/brain.md` unter „vermeiden" eintragen, mit Datum und Lauf-ID.
