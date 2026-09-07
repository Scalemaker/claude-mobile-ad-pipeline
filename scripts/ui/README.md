# Cockpit

Eine lokale Seite für genau einen Zweck: einen Pipeline-Lauf ansehen, freigeben, rendern lassen, Ergebnis prüfen.

```bash
python3 scripts/ui.py            # http://127.0.0.1:7788
python3 scripts/ui.py --port 8000
```

![Das Cockpit mit dem mitgelieferten STUR-Lauf](../../docs/post/cockpit.png)

## Was sie tut

| Bereich | Inhalt |
|---|---|
| links | `source.md`, `teardown.md`, `rebuild.md` des Laufs, als Text gesetzt |
| Freigabe | die Summe aus `cost.md` und ein Knopf. Der Klick schreibt `approved.json` in den Lauf |
| Render | Status je Format aus `render.json`, aktualisiert sich von selbst |
| Ergebnis | die gekennzeichneten Clips zum Abspielen, dazu ein Kontaktblatt |

## Was sie nicht tut

- **Sie denkt nicht.** Teardown und Rebuild schreibt Claude Code in den Lauf-Ordner. Die Seite liest sie nur.
- **Sie gibt nichts von allein aus.** Der Render startet erst nach Klick, und nur wenn `approved.json` und `prompts.json` da sind. Beides wird serverseitig geprüft, nicht im Browser.
- **Sie kennzeichnet nicht.** Das läuft über den MCP in Claude Code, siehe `/label`.
- **Sie ist nicht aus dem Netz erreichbar.** Der Server bindet an 127.0.0.1.

## Läufe

Angezeigt wird alles unter `runs/` und die Beispiele unter `examples/`, sofern eine `source.md` darin liegt. Beispiel-Läufe sind schreibgeschützt, damit niemand versehentlich einen Render auf fremden Daten startet. Ein einzelner Lauf ist als Lesezeichen erreichbar: `http://127.0.0.1:7788/#<lauf-id>`.

## Anpassen

Alles steckt in zwei Dateien: `scripts/ui.py` (Server, Standardbibliothek) und `scripts/ui/index.html` (Seite, kein Framework). Wer eine Spalte anders will, ändert das HTML und lädt neu.
