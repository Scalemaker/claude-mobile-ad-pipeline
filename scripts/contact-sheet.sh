#!/usr/bin/env bash
# Kontaktblatt für einen Clip: drei Frames (Anfang, Mitte, Ende) nebeneinander,
# bei Hochformat mit eingezeichneter Reels-Safe-Zone, plus Nachweis der
# XMP-Markierung im File.
#
#   scripts/contact-sheet.sh clip.mp4 [out.jpg] [--no-zone]
#
# Safe-Zone-Geometrie: Bruchteile der Framegröße aus der Figma-Community-Datei
# „Meta Ads Frames — Safe Zones" (File-Key fhS4nFVyOGm14IRPBh8sum), ausgelesen
# am 11.08.2026. Reels ist kein Rechteck: die Aktionsleiste rechts ragt von
# 56,6 % Höhe abwärts in die Zone. Nutzbar ist ein L.
set -euo pipefail
IN="${1:?Clip fehlt}"
OUT="${2:-${IN%.*}-sheet.jpg}"
ZONE=1
for a in "$@"; do [ "$a" = "--no-zone" ] && ZONE=0; done

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width  -of csv=p=0 "$IN")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$IN")
T1=0.2
T2=$(python3 -c "print(round($DUR/2,2))")
T3=$(python3 -c "print(round(max(0,$DUR-0.3),2))")

# Reels 9:16, Bruchteile: links 0.060185, oben 0.140625, rechts 0.939815,
# rechter Teil bis 0.566146, linker Teil bis 0.65, Leiste ab x 0.819444 bis y 0.966146
FILTER="null"
if [ "$ZONE" -eq 1 ] && [ "$H" -gt "$W" ]; then
  FILTER="drawbox=x=iw*0.060185:y=ih*0.140625:w=iw*0.87963:h=ih*0.425521:color=lime@0.9:t=4,\
drawbox=x=iw*0.060185:y=ih*0.566146:w=iw*0.759259:h=ih*0.083854:color=lime@0.9:t=4,\
drawbox=x=iw*0.819444:y=ih*0.566146:w=iw*0.120371:h=ih*0.4:color=red@0.8:t=4"
fi

TMP=$(mktemp -d)
i=0
for T in "$T1" "$T2" "$T3"; do
  i=$((i+1))
  ffmpeg -y -loglevel error -ss "$T" -i "$IN" -frames:v 1 -vf "$FILTER" "$TMP/f$i.png"
done
ffmpeg -y -loglevel error -i "$TMP/f1.png" -i "$TMP/f2.png" -i "$TMP/f3.png" \
  -filter_complex "[0][1][2]hstack=inputs=3" -q:v 3 "$OUT"
rm -rf "$TMP"

echo "Clip:        $IN (${W}x${H}, ${DUR}s)"
if strings "$IN" | grep -q "Iptc4xmpExt:DigitalSourceType"; then
  echo "Markierung:  XMP/IPTC DigitalSourceType vorhanden"
else
  echo "Markierung:  FEHLT, Clip ist nicht maschinenlesbar gekennzeichnet"
fi
[ "$FILTER" = "null" ] && echo "Safe Zone:   nicht eingezeichnet (Querformat oder --no-zone)" || echo "Safe Zone:   grün = nutzbar, rot = Reels-Aktionsleiste"
echo "Kontaktblatt: $OUT"
