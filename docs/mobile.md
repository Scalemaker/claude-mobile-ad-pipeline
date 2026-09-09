# Vom Handy aus

Drei Wege, die heute funktionieren. Alle drei sind Standardfunktionen, nichts davon ist ein Hack. Was sie nicht können, steht dabei.

## Weg 1 · Claude Code mit Remote Control

Der Mac bleibt zu Hause an, du nimmst die Session mit.

```bash
cd claude-mobile-ad-pipeline
claude --remote-control
```

Danach erscheint die Session in der Claude-App auf dem Handy. Du schreibst dort wie im Terminal: `/pipeline <ad> --marke demo`. Claude Code arbeitet auf dem Mac, mit den MCP-Servern und Skripten dieses Repos. Wenn ein Halt erreicht ist (Briefing bereit, Preis steht), schickt Claude eine Push-Nachricht ans Handy. Du liest, antwortest `freigeben`, gehst weiter.

Was das kann: alles aus diesem Repo, inklusive Kontaktblatt und Skripte, weil es auf dem Mac läuft.
Was das braucht: der Mac ist an, nicht im Ruhezustand, und online.
Was das nicht kann: wenn die Verbindung abreißt, kommt keine Push mehr. Die Session läuft trotzdem weiter, du siehst den Stand beim nächsten Öffnen.

## Weg 2 · Claude-App mit Projekt

Ganz ohne Mac.

1. In der Claude-App ein Projekt anlegen: „Ad Pipeline · <Marke>".
2. Den Text aus `prompts/orchestrator-system-prompt.md` als Projektanweisung einfügen.
3. Die neun Dateien aus `brand/<marke>/` als Projektwissen hochladen.
4. Den Connector Higgsfield im Projekt aktivieren.

Dann: Ad in den Projektchat, Claude macht Teardown und Rebuild, du schreibst `freigeben`, Claude holt den Preis, du schreibst `freigeben`, Claude ruft Higgsfield auf. Alles in einem Chat.

Was das kann: Teardown, Rebuild, Render.
Was das nicht kann: die Skripte (Kontaktblatt, Bibliothekspflege) laufen dort nicht, und `brain.md` musst du von Hand ins Projektwissen zurückspielen. Claude schlägt die Zeilen am Ende jedes Laufs vor.
Was du wissen solltest: Der Chat wartet nicht im Hintergrund. Wenn ein Render länger dauert, schreibst du „status", und Claude fragt den Stand ab.

## Weg 3 · Routine

Für den Fall, dass du nicht einmal die Ad selbst reinwerfen willst.

Eine Cloud-Routine in Claude Code läuft zu fester Zeit, liest eine Watchlist (`runs/watchlist.md` mit Ad-Library-Links, die du unterwegs ergänzt), macht für jeden Eintrag Teardown und Rebuild und legt die Briefings in `runs/` ab. Du findest morgens fertige Briefings vor und gibst frei, was dir gefällt.

Was das kann: Schritt 1 und 2 ohne dich.
Was das bewusst nicht kann: rendern. Der Halt vor dem Geldausgeben bleibt, und er bleibt bei dir.

## Push-Nachrichten

Claude Code schickt Push-Nachrichten nur, wenn Remote Control verbunden ist, und nur an zwei Stellen: Briefing bereit, Clips fertig. Nicht für Zwischenschritte. Wer bei jedem Job eine Nachricht bekommt, schaltet sie nach zwei Tagen ab.
