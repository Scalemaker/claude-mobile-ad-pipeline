#!/usr/bin/env bash
# Prüft, ob alles da ist, was die Pipeline braucht. Ändert nichts.
set -u
ok=0; bad=0
pass() { echo "  ok   $1"; ok=$((ok+1)); }
fail() { echo "  FEHLT $1"; bad=$((bad+1)); }

echo "Werkzeuge"
command -v claude  >/dev/null && pass "claude (Claude Code)"   || fail "claude: https://claude.com/claude-code"
command -v ffmpeg  >/dev/null && pass "ffmpeg"                 || fail "ffmpeg: brew install ffmpeg"
command -v ffprobe >/dev/null && pass "ffprobe"                || fail "ffprobe (kommt mit ffmpeg)"
command -v python3 >/dev/null && pass "python3"                || fail "python3"

echo "MCP-Server (claude mcp list)"
if command -v claude >/dev/null; then
  list=$(claude mcp list 2>/dev/null)
  echo "$list" | grep -qi "higgsfield"       && pass "higgsfield verbunden"       || fail "higgsfield: im Repo 'claude' starten und die Server aus .mcp.json bestätigen, dann Browser-Login"
  echo "$list" | grep -qi "ki-kennzeichnung" && pass "ki-kennzeichnung verbunden" || fail "ki-kennzeichnung: wie oben"
  echo "$list" | grep -qiE "higgsfield.*(Needs authentication|Fehler|failed)" && fail "higgsfield braucht Login: ein Tool einmal aufrufen, Browser öffnet sich"
fi

echo "Markenkontext"
shopt -s nullglob
brands=(../brand/*/)
brands=("${brands[@]/#..\/brand\/_template\//}")
found=0
for b in ../brand/*/; do
  n=$(basename "$b"); [ "$n" = "_template" ] && continue
  found=1
  missing=""
  for f in voice_core product_core icp_core aesthetic_core ad_library_last_90_days winning_hooks shipped_scripts brain assets; do
    [ -f "$b/$f.md" ] || missing="$missing $f.md"
  done
  if [ -z "$missing" ]; then pass "brand/$n vollständig"; else fail "brand/$n, es fehlen:$missing"; fi
  grep -q "<!--" "$b/product_core.md" 2>/dev/null && echo "  Hinweis: brand/$n/product_core.md hat noch Vorlagen-Kommentare"
done
[ $found -eq 0 ] && fail "keine Marke angelegt: /brand-setup in Claude Code ausführen"

echo
echo "$ok ok, $bad offen"
[ $bad -eq 0 ]
