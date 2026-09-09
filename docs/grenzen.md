# Grenzen, ehrlich

Was hier steht, ist gemessen oder aus den Werkzeugen selbst abgelesen. Was nicht gemessen ist, steht als offen.

## Rendern

- **Deutsche Dialoge in Seedance 2.0 nur als Kurzsätze.** Gemessen am 06.09.2026 (STUR-Lauf): ein 33-Wörter-Text kam als Brei zurück, zwei- bis dreiwörtige Sätze („Nie wieder.", „50 Jahre Garantie.") sauber, beides per Whisper gegengeprüft. Hook und Proof gehören als Untertitel in den Schnitt, nicht in den Mund des Modells.

- **Der Preis steht vor dem Lauf fest, nicht in diesem Repo.** `generate_video` mit `get_cost: true` nennt die Credits je Format, bevor etwas gestartet wird. Wir schreiben hier keine Kostenzahl hin, weil sie sich mit Modell, Dauer und Auflösung ändert und du sie in fünf Sekunden selbst abfragst.
- **Die Modellliste ändert sich.** `seedance_2_0` ist die Vorgabe, weil es Referenzbilder für Produkt und Charakter nimmt und Ton erzeugt. `/render` prüft vor jedem Lauf mit `models_explore`, ob das noch stimmt.
- **Fünf Formate sind fünf Prompts, kein Schalter.** Ob sie sich unterscheiden, hängt an den Rahmen in `prompts/formats.md`. Wenn zwei Clips gleich aussehen, ist der Rahmen zu schwach, nicht das Modell.
- **Ausfälle gibt es.** Ein Job von fünf kann scheitern. `/render` reicht ihn einmal neu ein, dann meldet er ihn.
- **Eigener Quellclip nur zwischen 4 und 30 Sekunden.** Der Ad-Multiplier nimmt nichts außerhalb, und er kürzt nicht selbst.

## Kennzeichnen danach

- **Die Pipeline kennzeichnet nicht.** Sie endet beim gerenderten Clip. Das Setzen von EU-Icon und maschinenlesbarer Markierung machst du danach auf [ki-kennzeichnen.de](https://ki-kennzeichnen.de), nach dem Schnitt und vor dem Upload.
- **Metadaten überleben nicht jeden Weg.** Plattformen komprimieren beim Upload neu. Das sichtbare Icon bleibt, die maschinenlesbare Ebene kann verloren gehen. Deshalb beides setzen.
- **Ob dich eine Pflicht trifft, sagt dir kein Werkzeug.** Art. 50 EU AI Act kennt zwei Rollen mit zwei Pflichten. Das ist dein Einzelfall.

## Safe Zone

- **Die Werte sind ausgemessen, nicht aus Blogartikeln.** Quelle ist Metas Safe-Zone-Vorlage in Figma (Community-Datei, Stand 11.08.2026). Zusammengesuchte Werte lagen in unseren Tests in beide Richtungen daneben.
- **Reels ist ein L.** Die Aktionsleiste rechts ragt in die Zone. Das Kontaktblatt zeichnet sie rot ein.
- **Das Modell hält keine Zone ein.** Der Safe-Zone-Satz im Prompt hilft, garantiert nichts. Der Check passiert danach auf dem Kontaktblatt, nicht vorher im Prompt.

## Mobil

- **Weg 1 braucht einen wachen Mac.** Ruhezustand beendet die Session nicht, aber die Arbeit.
- **Weg 2 wartet nicht von allein.** Der Projektchat fragt den Render-Stand nur ab, wenn du „status" schreibst.
- **Push nur bei Remote Control.** Ohne Verbindung keine Nachricht.

## Offen

- Wie oft die fünf Formate im Erstversuch deutlich unterscheidbar sind. Wir haben es an einem Testlauf gesehen, nicht über zwanzig gemessen.
- Ob `ai-modified` beim Ad-Multiplier immer die richtige Wahl ist, wenn nur der Hintergrund getauscht wurde. Wir setzen es so, weil echtes Material bearbeitet wurde.
