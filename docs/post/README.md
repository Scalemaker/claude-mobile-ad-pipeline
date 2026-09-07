# Post-Grafik

`mockup.html` ist die LinkedIn-Post-Grafik als HTML, `mockup.png` die gerenderte Fassung (1080×1350, 2x). Die Kacheln sind echte Frames aus `examples/stur-run/final/`, mit dem eingebrannten EU-Icon. Die Wettbewerber-Ad ist bewusst ein Platzhalter, kein Frame aus dem HexClad-Video.

Neu rendern nach Änderungen:

```bash
node scripts/render-html.mjs docs/post/mockup.html docs/post/mockup.png 1080 1350 2
```

Das Kommentar-Keyword im CTA ist ein Platzhalter, bis der Post steht.
