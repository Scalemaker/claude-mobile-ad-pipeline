---
name: teardown
description: Zerlegt eine Wettbewerber-Ad in Hook, Überzeugungsmechanik, emotionalen Bogen und Belief Shift. Verwenden, wenn eine Ad als Link, Screenshot oder Transkript reinkommt und das Ergebnis als Grundlage für einen Rebuild dienen soll.
---

# /teardown <ad> --marke <marke>

## Eingabe

Eine von drei Formen:
- Link (Meta Ad Library, TikTok, YouTube). Seite im Browser öffnen, Text und sichtbare Frames erfassen. Wenn die Seite nicht lesbar ist, das sagen und um Screenshot plus Transkript bitten. Nicht raten.
- Screenshot plus Transkript, vom Operator eingefügt.
- Nur Transkript. Dann fehlt die Bildebene, das steht im Teardown als Einschränkung.

## Ablauf

1. `brand/<marke>/icp_core.md` lesen. Teil 1 des Teardowns bezieht sich auf diesen Zielkunden, nicht auf einen allgemeinen.
2. Lauf-Ordner anlegen: `runs/<YYYY-MM-DD>-<slug>/`. Slug aus Wettbewerber und Hook, kurz. Eingabe als `source.md` ablegen: Quelle, Transkript, Beschreibung der Frames.
3. Prompt aus `prompts/teardown.md` ausführen. Ausgabe nach `runs/<id>/teardown.md`.
4. Prüfen, bevor es weitergeht:
   - Steht die Quelle in Zeile 1?
   - Ist die Hook-Mechanik eine aus der 10er-Liste?
   - Hat Teil 3 Sekundenangaben?
   - Nennt Teil 4 einen konkreten Shot für den Wechsel?
   Wenn eine Prüfung scheitert, den Teil neu schreiben, nicht den ganzen Teardown.
5. Dem Operator die vier Teile zeigen, dann: „Weiter mit /rebuild?"

## Ausgabe

`runs/<id>/teardown.md` mit genau vier Überschriften: `## Teil 1 · Hook`, `## Teil 2 · Mechanik`, `## Teil 3 · Emotionaler Bogen`, `## Teil 4 · Belief Shift`.

## Was der Teardown nicht tut

- Keine Kennzahlen zur Wettbewerber-Ad schätzen. Laufzeit aus der Ad Library ist ein Fakt, Reichweite meistens nicht.
- Keine Bewertung „gute Ad / schlechte Ad". Der Operator hat sie als Gewinner reingegeben, das ist die Prämisse.
