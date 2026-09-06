# Grenzen, ehrlich

Was hier steht, ist gemessen oder aus den Werkzeugen selbst abgelesen. Was nicht gemessen ist, steht als offen.

## Rendern

- **Der Preis steht vor dem Lauf fest, nicht in diesem Repo.** `generate_video` mit `get_cost: true` nennt die Credits je Format, bevor etwas gestartet wird. Wir schreiben hier keine Kostenzahl hin, weil sie sich mit Modell, Dauer und Auflösung ändert und du sie in fünf Sekunden selbst abfragst.
- **Die Modellliste ändert sich.** `seedance_2_0` ist die Vorgabe, weil es Referenzbilder für Produkt und Charakter nimmt und Ton erzeugt. `/render` prüft vor jedem Lauf mit `models_explore`, ob das noch stimmt.
- **Fünf Formate sind fünf Prompts, kein Schalter.** Ob sie sich unterscheiden, hängt an den Rahmen in `prompts/formats.md`. Wenn zwei Clips gleich aussehen, ist der Rahmen zu schwach, nicht das Modell.
- **Ausfälle gibt es.** Ein Job von fünf kann scheitern. `/render` reicht ihn einmal neu ein, dann meldet er ihn.
- **Eigener Quellclip nur zwischen 4 und 30 Sekunden.** Der Ad-Multiplier nimmt nichts außerhalb, und er kürzt nicht selbst.

## Kennzeichnung

- **Icon und Markierung sind ein Input, kein Urteil.** Der Skill setzt das EU-Icon ins Bild und `DigitalSourceType` als XMP/IPTC ins File. Geprüft an einem Testclip am 06.09.2026: Icon gesetzt, XMP im File nachweisbar. Ob deine Veröffentlichung damit alle Pflichten erfüllt, hängt von deiner Rolle und dem Inhalt ab. Das steht so auch im Tool.
- **Metadaten überleben nicht jeden Weg.** Plattformen komprimieren beim Upload neu. Das sichtbare Icon bleibt, die XMP-Ebene kann verloren gehen. Deshalb beides, und deshalb das Register als Nachweis, falls du es brauchst.

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
