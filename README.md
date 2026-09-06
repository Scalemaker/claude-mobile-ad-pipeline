# Mobile Ad Pipeline: Claude Code + Higgsfield MCP + KI-Kennzeichnung

Eine Winner-Ad des Wettbewerbers rein, fünf fertige und gekennzeichnete 9:16-Clips für dein eigenes Produkt raus. Du steuerst die Pipeline vom Handy, das Rendern läuft über den Higgsfield-MCP, die Kennzeichnung nach Art. 50 EU AI Act über den KI-Kennzeichnung-MCP. Der Laptop kommt erst am Ende für den Feinschliff ins Spiel.

Dieses Repo ist der komplette Bausatz: sechs Claude-Code-Skills, die Markenkontext-Vorlagen, der Orchestrator-Prompt für die Claude-App am Handy, die Prüfskripte und ein durchgerechneter Beispiel-Lauf.

## Was die Pipeline macht

| Schritt | Skill | Was passiert | Wo du bist |
|---|---|---|---|
| 1 | `/teardown` | Zerlegt die Wettbewerber-Ad in Hook, Mechanik, emotionalen Bogen und Belief Shift | Handy |
| 2 | `/rebuild` | Baut auf denselben Knochen ein 6-Shot-Storyboard für dein Produkt, in deiner Stimme | Handy |
| 3 | Freigabe | Du liest das Briefing, antwortest `freigeben`. Vorher siehst du den Preis, den Higgsfield für die Renders nimmt | Handy |
| 4 | `/render` | Fünf Format-Varianten über den Higgsfield-MCP: UGC, Cinematic, Reaction, Mirror-Hook, Split-Screen | unterwegs |
| 5 | `/label` | Jeder Clip bekommt das offizielle EU-Icon und die maschinenlesbare XMP/IPTC-Markierung über den KI-Kennzeichnung-MCP, platziert innerhalb der Reels-Safe-Zone | unterwegs |
| 6 | Prüfen | Kontaktblatt pro Clip mit eingezeichneter Safe Zone, Markierung wird im File nachgewiesen. Dann Schnittprogramm und Meta-Entwurf | Laptop |

`/pipeline` fährt die Schritte 1 bis 5 in einem Zug und hält nur vor dem Geldausgeben an.

## Schnellstart

Du brauchst: [Claude Code](https://claude.com/claude-code), einen Higgsfield-Account, `ffmpeg` (`brew install ffmpeg`) und Python 3.

```bash
git clone https://github.com/Scalemaker/claude-mobile-ad-pipeline.git
cd claude-mobile-ad-pipeline
claude
```

Beim ersten Start fragt Claude Code, ob es die beiden MCP-Server aus `.mcp.json` laden darf. Ja sagen. Beide laufen über OAuth: beim ersten Aufruf eines Tools öffnet sich der Browser zum Login, danach ist der Server verbunden.

Dann im Chat:

```
/brand-setup
```

Der Skill fragt dich die Markenwerte ab und legt `brand/<marke>/` aus den Vorlagen an. Was du an Ad-Historie hast (letzte Gewinner, Hooks, Skripte), kommt in die Dateien dort. Ohne diese Dateien schreibt die Pipeline Ads, die nach niemandem klingen.

Einrichtung prüfen:

```bash
scripts/check-setup.sh
```

## So sieht ein Lauf aus

```
/pipeline https://www.facebook.com/ads/library/?id=... --marke demo
```

oder mit einem Screenshot plus Transkript, wenn du die Ad nur als Bild hast. Alles, was ein Lauf erzeugt, liegt danach in `runs/<datum>-<slug>/`:

```
runs/2026-09-06-demo/
├── source.md         die Ad, wie du sie reingegeben hast
├── teardown.md       die vier Teile
├── rebuild.md        Hook, Storyboard, Voiceover, Locks
├── cost.md           was Higgsfield vor der Freigabe als Preis genannt hat
├── render.json       Job-IDs und Ergebnis-URLs je Format
└── final/            gekennzeichnete Clips plus Kontaktblätter
```

## Vom Handy aus

Drei Wege, alle drei funktionieren heute, keiner braucht einen Trick. Ausführlich in [docs/mobile.md](docs/mobile.md).

1. **Claude Code mit Remote Control.** Auf dem Mac `claude --remote-control` starten, dann die Session in der Claude-App am Handy übernehmen. Freigaben und Rückfragen laufen als Push auf dein Handy, solange die Verbindung steht.
2. **Claude-App mit Projekt.** Den Prompt aus `prompts/orchestrator-system-prompt.md` als Projektanweisung, die Markendateien als Projektwissen, Higgsfield und KI-Kennzeichnung als Connectoren. Läuft komplett am Handy, ohne Mac.
3. **Routine.** Ein Cloud-Lauf zu fester Uhrzeit, der eine Watchlist an Ads abarbeitet und dir die Briefings zur Freigabe hinlegt.

## So sieht die Prüfung aus

![Kontaktblatt eines gekennzeichneten Testclips](docs/kontaktblatt-beispiel.jpg)

Grün ist die nutzbare Reels-Zone, rot die Aktionsleiste, links oben das EU-Icon, gesetzt über den KI-Kennzeichnung-MCP. Der Clip dazu liegt als `docs/safe-zone-testclip-labeled.mp4` im Repo, die Rohfassung daneben. Probier es aus:

```bash
scripts/contact-sheet.sh docs/safe-zone-testclip-labeled.mp4
```

## Was diese Pipeline von der Vorlage unterscheidet

Die Idee, eine Wettbewerber-Ad zu zerlegen und um das eigene Produkt neu zu bauen, ist nicht neu. Drei Dinge sind hier anders:

- **Kennzeichnung ist ein Pipeline-Schritt, keine Nachfrage.** Seit dem 2. August 2026 gilt Art. 50 EU AI Act. Welche Pflicht dich trifft, hängt von deiner Rolle ab. Die Pipeline setzt Icon und Markierung auf jeden Clip, bevor er den Ordner verlässt. Ob damit deine Pflicht erfüllt ist, entscheidet dein Einzelfall, nicht ein Tool.
- **Safe Zone ist Geometrie, keine Bitte.** Icon und Kontaktblatt arbeiten mit den ausgemessenen Meta-Safe-Zones. Reels ist dabei kein Rechteck, sondern ein L, weil die Aktionsleiste rechts hineinragt.
- **Formate sind schwache Diversifikation.** Fünf Formate derselben Idee sind für Metas Auslieferung ein Kandidat mit fünf Gesichtern. `/rebuild --angles` baut stattdessen drei Rebuilds entlang der Kern-Angles Pain, Benefit, Proof. Das sind drei Kandidaten.

Ehrliche Grenzen stehen in [docs/grenzen.md](docs/grenzen.md), die typischen Fehler samt Fix in [docs/fehler-und-fixes.md](docs/fehler-und-fixes.md).

## Aufbau

```
.claude/skills/     brand-setup, teardown, rebuild, render, label, pipeline
.mcp.json           Higgsfield-MCP und KI-Kennzeichnung-MCP, Projekt-Scope
CLAUDE.md           die Regeln, nach denen Claude Code hier arbeitet
brand/_template/    die acht Markendateien als Vorlage
prompts/            Orchestrator-Prompt (Handy), Teardown, Rebuild, Format-Rahmen
scripts/            check-setup, contact-sheet, rotate-library
docs/               mobile, grenzen, fehler-und-fixes
examples/demo-run/  ein vollständiger Teardown plus Rebuild zum Nachlesen
```

## Lizenz

MIT. Die EU-Icons gehören der Europäischen Kommission und kommen über den KI-Kennzeichnung-MCP.

Gebaut von [Scalemaker](https://scalemaker.de). Das Kennzeichnungs-Tool dahinter: [ki-kennzeichnen.de](https://ki-kennzeichnen.de).
