#!/usr/bin/env bash
# Prüft, ob alles da ist, was die Pipeline braucht. Ändert nichts.
# Läuft von überall: alle Pfade hängen am Skript, nicht am Arbeitsverzeichnis.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ok=0; bad=0; warn=0
pass() { echo "  ok    $1"; ok=$((ok+1)); }
fail() { echo "  FEHLT $1"; bad=$((bad+1)); }
note() { echo "        $1"; }
soft() { echo "  offen $1"; warn=$((warn+1)); }

echo "Werkzeuge"
command -v claude  >/dev/null && pass "claude (Claude Code)"   || fail "claude: https://claude.com/claude-code"
command -v ffmpeg  >/dev/null && pass "ffmpeg"                 || fail "ffmpeg: brew install ffmpeg"
command -v ffprobe >/dev/null && pass "ffprobe"                || fail "ffprobe (kommt mit ffmpeg)"
command -v python3 >/dev/null && pass "python3"                || fail "python3"

echo "Render-Route (mindestens eine reicht)"
routes=0
if [ -f "$ROOT/.env" ] && grep -qE '^FAL_KEY=.+' "$ROOT/.env"; then
  # letzte nicht-leere Zuweisung gewinnt, damit die leere Zeile aus .env.example nicht stört
  key=$(grep -E '^FAL_KEY=.+' "$ROOT/.env" | tail -1 | cut -d= -f2- | tr -d '"'"'"'' | tr -d '[:space:]')
  bal=$(curl -s -m 10 -H "Authorization: Key $key" https://rest.alpha.fal.ai/billing/user_balance 2>/dev/null)
  if printf '%s' "$bal" | grep -qE '^-?[0-9]+([.][0-9]+)?$'; then
    pass "fal.ai erreichbar, Guthaben $(printf '%.2f' "$bal") \$"; routes=$((routes+1))
    awk -v b="$bal" 'BEGIN{ if (b+0 < 5) exit 0; exit 1 }' && note "unter 5 \$, das reicht für etwa einen Lauf mit fünf Clips"
  else
    fail "FAL_KEY in .env, aber fal antwortet nicht wie erwartet: ${bal:-keine Antwort}"
    note "Key prüfen auf fal.ai/dashboard/keys, die Zeile in .env muss FAL_KEY=<key> lauten"
  fi
else
  soft "fal.ai: kein FAL_KEY in .env (Route \`/render --provider fal\`, in diesem Repo verifiziert)"
  note "Key holen: fal.ai/dashboard/keys, dann 'cp .env.example .env' und eintragen"
fi
if command -v claude >/dev/null; then
  list=$(claude mcp list 2>/dev/null)
  if echo "$list" | grep -qi "higgsfield"; then
    pass "higgsfield-MCP eingetragen (Route \`/render\`, Standard)"; routes=$((routes+1))
  else
    soft "higgsfield-MCP nicht verbunden (im Repo 'claude' starten, Server aus .mcp.json bestätigen, dann Browser-Login)"
  fi
fi
[ "$routes" -eq 0 ] && fail "keine Render-Route einsatzbereit: entweder FAL_KEY eintragen oder Higgsfield verbinden"

echo "Markenkontext"
found=0
for b in "$ROOT"/brand/*/; do
  n=$(basename "$b"); [ "$n" = "_template" ] && continue
  found=1
  missing=""
  for f in voice_core product_core icp_core aesthetic_core ad_library_last_90_days winning_hooks shipped_scripts brain assets; do
    [ -f "$b/$f.md" ] || missing="$missing $f.md"
  done
  if [ -z "$missing" ]; then pass "brand/$n vollständig"; else fail "brand/$n, es fehlen:$missing"; fi
  if grep -q "<!--" "$b/product_core.md" 2>/dev/null; then
    note "brand/$n/product_core.md hat noch Vorlagen-Kommentare, also ungefüllte Abschnitte"
  fi
done
[ $found -eq 0 ] && fail "keine Marke angelegt: Claude Code im Repo starten und /brand-setup aufrufen"

echo
echo "$ok ok, $warn offen, $bad fehlend"
[ $bad -eq 0 ]
