# Rebuild-Prompt

Wird von `/rebuild` verwendet, direkt nach dem Teardown. Liest `brand/<marke>/` komplett.

```
Bau die Ad jetzt um [HERO_SKU aus product_core.md] neu.

BEHALTEN AUS DEM TEARDOWN
- Hook-Mechanik: [Teil 1]
- Überzeugungsmechanik: [Teil 2]
- Form des emotionalen Bogens: [Teil 3]
- Belief-Shift-Struktur: [Teil 4]

NEU FÜR UNSER PRODUKT
- Hook-Zeile: neu, in der Stimme aus voice_core.md, gleiche Mechanik,
  unter 12 Wörtern
- Skript: 6-Shot-Storyboard um unseren Zielkunden aus icp_core.md und
  die belegten Aussagen aus product_core.md
- Charakter: aus assets.md (Higgsfield-Element), sonst Beschreibung
  aus aesthetic_core.md
- Produktmoment: die natürlichen Nutzungsmomente aus product_core.md
- Emotionale Beats: gleiche Form, aber unsere Auslöser

AUSGABE
1. Neue Hook-Zeile
2. 6-Shot-Storyboard als Tabelle: Shot · Bild · Kamera · Ton · Overlay · Dauer
3. Voiceover mit Sprechanweisung, falls nötig
4. Locks: Produkt-Element, Charakter-Element, Safe-Zone-Hinweis für Overlays
   (Reels: Text nur im oberen Bereich der Safe Zone, rechts unten liegt die
   Aktionsleiste)
5. Quellen: welche Einträge aus ad_library_last_90_days.md und
   winning_hooks.md als Vorbild dienten
6. Jede Produktaussage mit Beleg aus product_core.md. Ohne Beleg: TODO.

Danach: „Briefing bereit. Antworte mit `freigeben`, dann zeige ich dir
den Preis für fünf Formate und starte den Render nach deiner zweiten
Freigabe."

Kein Gedankenstrich. Keine Sätze mit „Die meisten…". Keine erfundenen
Zahlen.
```

## Variante `--angles`

Statt fünf Formaten derselben Idee: drei Rebuilds entlang der Kern-Angles. Metas Auslieferung behandelt konzeptionell verschiedene Ads als eigene Kandidaten, Formatvarianten derselben Idee nicht.

```
Bau drei Rebuilds, jeder mit eigenem Angle. Alle drei behalten die
Teardown-Knochen, unterscheiden sich aber in dem, worum die Ad kreist:

1. PAIN: die Frustration aus icp_core.md „Was ihn stoppt", der Hook
   benennt den Schmerz
2. BENEFIT: der Wunschzustand aus „Was er will", der Hook zeigt das Ergebnis
3. PROOF: ein belegter Beweis aus product_core.md, der Hook ist der Beweis

Je Rebuild dieselbe Ausgabe wie oben. Nummerier die Läufe angle-pain,
angle-benefit, angle-proof.
```
