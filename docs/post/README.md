# Grafiken fürs Ausspielen

Beide sind HTML, gerendert per CDP. Die Kacheln sind echte Frames aus `examples/stur-run/final/`, mit dem eingebrannten EU-Icon.

| Datei | Wofür | Rendern |
|---|---|---|
| `mockup.html` → `mockup.png` | LinkedIn-Post, 1080×1350 | `node scripts/render-html.mjs docs/post/mockup.html docs/post/mockup.png 1080 1350 2` |
| `ablauf.html` → `ablauf.png` | „So wird sie benutzt", für Notion und Website | `node scripts/render-html.mjs docs/post/ablauf.html docs/post/ablauf.png 1080 auto 2` |

`auto` als Höhe misst die Dokumenthöhe, damit unten nichts abgeschnitten wird.

Der Ablauf zeigt den echten STUR-Lauf, gekürzt auf das, was am Schirm steht. Das Kommentar-Keyword im Post-CTA ist ein Platzhalter, bis der Post steht.
