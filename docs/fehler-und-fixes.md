# Typische Fehler und was hilft

**Der Rebuild klingt wie die Quelle.**
Zu nah am Text, zu weit weg von der Mechanik. Im Rebuild-Prompt steht „Knochen behalten, Inhalt neu". Test: beide Ads hintereinander lesen. Sagt jemand „kopiert", Hook und Sprache neu, Mechanik lassen.

**Der Rebuild hat die Wirkung der Quelle verloren.**
Er ist zu weit weg: eigener Hook, eigene Story, aber die Mechanik ist unterwegs verlorengegangen. Prüf gegen `teardown.md`, ob Hook-Mechanik, Überzeugungsmechanik, Form des Bogens und Belief-Shift-Struktur wirklich unverändert sind. Genau diese vier bleiben, alles andere wird neu. Wenn eine davon fehlt, den Rebuild noch einmal laufen lassen und die vier ausdrücklich benennen.

**Der Rebuild klingt nach niemandem.**
`brand/<marke>/` ist leer oder voller Vorlagen-Kommentare. `scripts/check-setup.sh` zeigt es. Ohne Ad-Historie und Stimme schreibt Claude Durchschnitt.

**Der Rebuild behauptet etwas, das das Produkt nicht kann.**
`product_core.md` „Belegte Aussagen" ist unvollständig oder veraltet. Nachziehen. Der Skill markiert unbelegte Aussagen als TODO, aber nur, wenn die Belegliste da ist, gegen die er prüft.

**Higgsfield antwortet mit 401 oder „Unauthorized".**
Der MCP-Server ist eingetragen, aber nicht eingeloggt. Ein beliebiges Higgsfield-Tool aufrufen, der Browser öffnet sich. Danach `claude mcp list`, dort muss „Connected" stehen.

**`generate_video_batch` kommt mit `unlim_choice` zurück.**
Kein Job wurde gestartet. Die Frage an den Operator weitergeben (Gratis-Kontingent oder Credits), dann denselben Aufruf mit `use_unlim` wiederholen. Nie selbst entscheiden.

**Fünf Clips sehen gleich aus.**
Die Rahmen in `prompts/formats.md` sind zu ähnlich formuliert oder das Storyboard dominiert den Prompt. Rahmen schärfen: UGC = Handkamera und Fensterlicht, Cinematic = Steadicam und Anamorph, Reaction = Gesicht frontal und Produkt von unten, Mirror = Zitat des Zielkunden in den ersten drei Sekunden, Split = zwei Bildhälften.

**Das Icon liegt unter der Reels-Aktionsleiste.**
`position: "bottom-right"` benutzt statt `x: 14, y: 20`. Neu kennzeichnen, das Kontaktblatt zeigt die Leiste rot.

**Das Kontaktblatt meldet „Markierung FEHLT".**
Der Clip wurde nach dem Kennzeichnen noch einmal durch ein Schnittprogramm exportiert. Reihenfolge: erst schneiden, dann kennzeichnen, dann hochladen. Oder die Datei ist noch die Higgsfield-Rohfassung.

**Ein Job von fünf bleibt „pending".**
`jobs_wait` mit `timeout_seconds: 15` erneut aufrufen, so oft es `poll_after_seconds` sagt. Nicht neu einreichen, solange der Job läuft.

**Keine Push-Nachricht am Handy.**
Remote Control nicht verbunden oder Mac im Ruhezustand. Session in der Claude-App öffnen, Stand steht im Chat.

**Der Schnitt frisst mehr Zeit als der Rest.**
Musik, Untertitel und Feinschliff jedes Mal von Hand zu setzen dauert länger als die ganze Pipeline davor. Leg dir im Schnittprogramm eine Vorlage an: Untertitelstil, Musikbett, Auf- und Abblende. Danach ist der letzte Schritt ein Anwenden statt eines Aufbaus. Wichtig bleibt die Reihenfolge: erst schneiden, dann kennzeichnen, dann hochladen.

**Der Operator gibt vier Stunden nicht frei.**
Kein Problem für die Pipeline. Sie wartet. Der Halt vor dem Geldausgeben ist Absicht, kein Fehler. Wer eine Erinnerung will, nutzt eine Routine, die offene Briefings morgens auflistet.
