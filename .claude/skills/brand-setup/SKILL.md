---
name: brand-setup
description: Legt den Markenkontext für die Ad-Pipeline an. Fragt Stimme, Produkt, Zielkunde und Bildsprache ab, kopiert die Vorlagen nach brand/<marke>/ und füllt sie. Verwenden bei der ersten Einrichtung oder wenn eine weitere Marke dazukommt.
---

# /brand-setup [marke]

## Ziel

Nach diesem Skill existiert `brand/<marke>/` mit allen neun Dateien aus `brand/_template/`, so weit gefüllt, dass `/rebuild` damit arbeiten kann.

## Ablauf

1. Wenn kein Name übergeben wurde: nach dem Markennamen fragen. Kleinbuchstaben, keine Leerzeichen.
2. `brand/_template/` nach `brand/<marke>/` kopieren. Existiert der Ordner schon, nichts überschreiben, sondern fragen, welche Datei nachgezogen werden soll.
3. Interview in genau dieser Reihenfolge, eine Frage pro Nachricht, damit es am Handy lesbar bleibt:
   - Produkt: Name, Preis, ein Satz, drei belegbare Aussagen mit Beleg
   - Zielkunde: wer, was er heute glaubt, was ihn stoppt, zwei Originalzitate
   - Stimme: drei Sätze aus echten Ads, die richtig klingen; Wörter, die gesperrt sind
   - Bildsprache: Licht, Setting, Charakter, was nie im Bild ist
   - Assets: URL des Produktbilds, falls vorhanden
4. Antworten in die jeweilige Datei eintragen. Kommentare in den Vorlagen entfernen, sobald der Abschnitt gefüllt ist. Leere Abschnitte bleiben mit Kommentar stehen.
5. Ad-Historie: fragen, ob es Gewinner-Ads der letzten 90 Tage gibt. Wenn ja, Format aus `ad_library_last_90_days.md` erklären und die ersten drei Einträge gemeinsam anlegen. Wenn nein, in `brain.md` unter „Offen" notieren: „Keine Ad-Historie beim Setup. Rebuilds laufen ohne Vorbilder, bis die ersten eigenen Ads geschaltet sind."
6. Zum Schluss `brand/<marke>/brain.md` mit einem ersten Eintrag unter „Offen" versehen: Datum, „Setup abgeschlossen, noch kein Lauf."

## Regeln

- Keine Aussage in `product_core.md` ohne Beleg. Lieber ein TODO als eine erfundene Zahl.
- Nichts aus dem Interview in andere Dateien schreiben. `brain.md` ist Lernprotokoll, kein Inhaltsverzeichnis.
