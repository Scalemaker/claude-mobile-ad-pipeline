# Lernprotokoll · STUR-Beispiel

## Funktioniert
- 2026-09-06 · stur-run · Der Produktfreisteller als `@Image1` reicht, damit Seedance 2.0 die STUR-Pfanne in allen fünf Formaten erkennbar hält: Draufsicht, glatter dunkler Boden, langer Gussgriff. Kein Charakter-Referenzbild nötig.
- 2026-09-06 · stur-run · Alle fünf Format-Rahmen aus `prompts/formats.md` haben sich im Erstversuch deutlich unterschieden: Handkamera-Küche, Anamorph mit Gasflamme, Gesicht-frontal mit Riech-Peak, statische Totale mit Zitat, Split oben/unten. Kein Cherry-Picking, je ein Lauf.
- 2026-09-06 · stur-run · Kurze deutsche Sätze (zwei bis drei Wörter) kommen aus Seedance 2.0 sauber: „Nie wieder Beschichtung.", „Nie wieder.", „50 Jahre Garantie." (per Whisper gegengeprüft).
- 2026-09-06 · stur-run · Das Beweisbild „Ei rutscht aus der Pfanne" funktioniert modellseitig zuverlässig, in vier von vier Prompts, die es enthielten.

## Vermeiden
- 2026-09-06 · stur-run · Längere deutsche Dialogzeilen in Seedance 2.0. Der 33-Wörter-Text des Rebuilds kam als Brei zurück („Beschaltung", „geiseelt", „Abgerecht und eingebählt", „Kein PFL"). Whisper-Transkript in `raw/`-Protokoll. Fix gemessen: Dialogformate nur mit ein bis zwei Kurzsätzen rendern, Hook und Proof als Untertitel im Schnitt setzen.
- 2026-09-06 · stur-run · Im Reaction-Clip hat das Modell dem Steak Grillstreifen gegeben, obwohl die STUR-Pfanne einen glatten Boden hat. Prompt-Fix für den nächsten Lauf: „flat smooth skillet, no grill marks".

## Offen
- Keine Kennzahlen zu STURs Ads, nur Laufzeit als Signal.
- Ob 1080p die Kruste und die Rillenoberfläche sichtbar besser zeigt. Nicht gemessen, 720p reichte für die Sichtung.
