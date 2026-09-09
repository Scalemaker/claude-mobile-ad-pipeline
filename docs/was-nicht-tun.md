# Was du damit nicht tun solltest

Die Skills haben harte Regeln, siehe `CLAUDE.md`. Das hier sind die Fehler, die dir die Pipeline nicht abnehmen kann, weil sie in deiner Hand liegen.

**Nicht ohne Markendateien starten.** Eine Pipeline ohne `brand/<marke>/` schreibt Ads, die nach jeder Marke klingen könnten. Die Ad-Historie ist der Unterschied zwischen deinem Rebuild und einem Durchschnitts-Rebuild. `scripts/check-setup.sh` sagt dir, was fehlt.

**Nicht ungelesen freigeben.** Der Freigabe-Knopf ist schnell, das ist Absicht. Trotzdem gilt: ein schlechtes Briefing wird ein schlechter Clip, und der Render kostet dasselbe.

**Den Teardown nicht überspringen.** Wer direkt umschreibt, kopiert die Oberfläche und lässt genau das liegen, was die Quelle wirken ließ. Mechanik, Bogen und Belief Shift sind der Grund, warum der Rebuild trägt.

**Nicht live schalten.** Die Pipeline endet beim gerenderten Clip. Schnitt, Kennzeichnung und der Upload zu Meta bleiben bei dir, und zwar als Entwurf mit einer letzten Sichtung.

**Nicht für lange Markenfilme.** Der Ablauf ist für Direct Response von etwa 15 bis 30 Sekunden gebaut. Ein erzählender Film von einer Minute lebt von anderen Dingen als von Hook-Mechanik und Belief Shift.

**Nicht dieselbe Marke an einem Tag mit vielen Teardowns fluten.** Die Varianz kommt aus verschiedenen Quellen und verschiedenen Angles, nicht aus der Menge. Wer fünf Wettbewerber-Ads hintereinander zerlegt, bekommt fünfmal ähnliche Rebuilds.

**Fünf Formate sind keine fünf Ads.** Sie sind eine Idee in fünf Kleidern. Wenn du echte Diversifikation für die Auslieferung brauchst, nimm `/rebuild --angles`, das baut drei Rebuilds entlang Pain, Benefit und Proof.

**Die Bibliothek nicht vergammeln lassen.** Eine `ad_library_last_90_days.md` mit sechs Monate alten Einträgen zieht den Rebuild in die Vergangenheit. Einmal die Woche `scripts/rotate-library.py`, das dauert eine Minute.

**Das Kennzeichnen nicht vergessen und nicht in der falschen Reihenfolge machen.** Die Clips sind vollständig KI-generiert. Kennzeichnen kommt nach dem Schnitt und vor dem Upload, auf [ki-kennzeichnen.de](https://ki-kennzeichnen.de). Ein Export danach wirft die maschinenlesbare Markierung wieder raus.

**Nicht so tun, als sei ein Werkzeug eine Rechtsauskunft.** Ob und welche Pflicht dich nach Art. 50 trifft, hängt an deiner Rolle und am Inhalt. Das entscheidest du oder deine Rechtsberatung.
