# Markenkontext

Pro Marke ein Ordner, angelegt von `/brand-setup` aus `_template/`. Die Ordner selbst sind per `.gitignore` ausgeschlossen, weil dort deine Ad-Historie liegt.

| Datei | Was drin steht | Pflege |
|---|---|---|
| `voice_core.md` | Stimme, Satzbau, gesperrte Wörter | quartalsweise |
| `product_core.md` | Hero-SKU, belegte Aussagen, Preis, Beweise | bei jeder Produktänderung |
| `icp_core.md` | Wer kauft, was er glaubt, was ihn stoppt | quartalsweise |
| `aesthetic_core.md` | Licht, Farben, Setting, was nie vorkommt | quartalsweise |
| `ad_library_last_90_days.md` | Jede geschaltete Ad der letzten 90 Tage mit Kennzahlen | wöchentlich, `scripts/rotate-library.py` |
| `winning_hooks.md` | Die Hooks, die skaliert haben, nach Mechanik gruppiert | monatlich |
| `shipped_scripts.md` | Volle Skripte oder Storyboards der letzten Ads | bei jedem Launch |
| `brain.md` | Lernprotokoll: funktioniert, vermeiden, offen | nach jedem Lauf |
| `assets.md` | Produktbild-URLs und Higgsfield-Element-IDs für Charakter und Produkt | bei Bedarf |

Das ist kein Fine-Tuning. Claude liest diese Dateien bei jedem Lauf komplett. Änderst du heute eine Zeile, gilt sie beim nächsten Lauf.
