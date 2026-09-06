# Die fünf Format-Rahmen

Wird von `/render` verwendet. Jeder Rahmen wird um das Storyboard aus `rebuild.md` gewickelt und als ein eigener Prompt an Higgsfield geschickt. Die Rahmen müssen sich deutlich unterscheiden, sonst kommen fünf Clips, die gleich aussehen.

Modell-Vorgabe: `seedance_2_0` (Referenzbilder für Produkt und Charakter, native Audio, 4 bis 15 Sekunden), `aspect_ratio: "9:16"`. Für 1080p oder 4K `mode: "std"`. Prüf die Parameter vor dem Lauf mit `models_explore action=get model_id=seedance_2_0`, das Modellangebot ändert sich.

Jeder Prompt endet mit dem Safe-Zone-Satz: `Keep all on-screen text and the product hero moment inside the upper two thirds of the frame; leave the lower right corner free.`

## 1 · UGC
```
Handheld iPhone footage, vertical 9:16, natural window light, slight camera
shake, creator talking to the front camera at arm's length, real skin
texture, no colour grading, ambient room sound. [STORYBOARD]
```

## 2 · Cinematic
```
Steadicam, 35mm anamorphic look, shallow depth of field, warm key light
with soft fill, subtle film grain, slow push-in on the product moment,
scored with a low ambient bed. [STORYBOARD]
```

## 3 · Reaction
```
Character faces the camera, product enters from below the frame at the
hook, hold on the face for the reveal, expression peaks exactly at the
belief-shift shot, tight framing, eye-level. [STORYBOARD]
```

## 4 · Mirror-Hook
```
Character speaks the viewer's inner monologue directly to camera in the
first three seconds, using the exact words from the ICP quotes, then
turns to the product. Static framing, no cuts in the first shot.
[STORYBOARD, Hook ersetzt durch ein Zitat aus icp_core.md „Wie er spricht"]
```

## 5 · Split-Screen
```
Vertical split screen: left side the old way (the pain), right side the
product in use, synchronised actions, hard cut to full frame on the
product at the belief-shift shot. [STORYBOARD]
```

## Kennzeichnung je Format

Alle fünf sind vollständig generiert: Icon `ai-generated-black` (oder `-white` auf dunklem Bild). Nur wenn ein eigener echter Quellclip über den Ad-Multiplier bearbeitet wurde, ist es `ai-modified-*`.
