---
name: pipeline
description: Fährt die komplette Ad-Pipeline in einem Zug, von der Wettbewerber-Ad bis zu fünf fertigen Clips, und hält nur zweimal an, jeweils vor dem Geldausgeben. Verwenden, wenn der Operator eine Ad reingibt und nicht jeden Schritt einzeln aufrufen will.
---

# /pipeline <ad> --marke <marke> [--angles] [--formate …]

`--lauf <id>` statt `<ad>` nimmt einen Lauf, den das Cockpit schon angelegt hat. Quelle steht dann in `runs/<id>/source.md`.

## Ablauf

1. `/teardown <ad> --marke <marke>`
2. `/rebuild --marke <marke>` (mit `--angles`, wenn übergeben)
3. **Halt 1.** Briefing zeigen, auf `freigeben` warten. Alles andere ist ein Nein. Bei „ändere X" die Änderung einarbeiten, Briefing neu zeigen, wieder warten.
4. `/render --marke <marke>` bis zum Preis
5. **Halt 2.** Preis zeigen, auf `freigeben` warten.
6. `/render` fertig fahren.
7. Übergabe: die Clips auflisten, ein Satz je Format, welches am ehesten zum Angebot passt. Dann der nächste Schritt am Laptop, in dieser Reihenfolge:
   - Schnittprogramm: Musik, Untertitel, Feinschliff, Export
   - Kennzeichnen auf [ki-kennzeichnen.de](https://ki-kennzeichnen.de): EU-Icon und maschinenlesbare Markierung setzen, kostenlos und ohne Anmeldung
   - Meta als Entwurf, letzte Sichtung, dann live
   Die Reihenfolge ist wichtig: erst schneiden, dann kennzeichnen. Ein Export nach dem Kennzeichnen wirft die Markierung wieder raus.
8. Drei Zeilen für `brand/<marke>/brain.md` vorschlagen und nach Bestätigung eintragen.

## Zeitverhalten

Der Operator ist zwischen den Halts nicht am Gerät. Deshalb:
- Vor jedem Halt eine Push-Nachricht, wenn Remote Control verbunden ist.
- Kein Halt ohne klare Frage in der letzten Zeile.
- Bei Fehlern in Schritt 4 bis 6 nicht abbrechen, sondern das betroffene Format melden und die anderen fertigstellen.

## Mit --angles

Schritt 2 liefert drei Storyboards. Halt 1 zeigt alle drei, der Operator wählt eins, zwei oder alle. Jedes gewählte Storyboard läuft durch Schritt 4 bis 6 in einem eigenen Unterordner `runs/<id>/angle-<name>/`. Der Preis in Halt 2 ist die Summe über alle gewählten.
