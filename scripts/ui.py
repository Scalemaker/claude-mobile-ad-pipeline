#!/usr/bin/env python3
"""Cockpit für einen Pipeline-Lauf. Lesen, freigeben, rendern, ansehen.

    python3 scripts/ui.py            # http://127.0.0.1:7788
    python3 scripts/ui.py --port 8000

Kein npm, keine Abhängigkeiten, nur die Standardbibliothek. Bindet ausschliesslich
an 127.0.0.1, ist also nicht aus dem Netz erreichbar.

Was die Seite NICHT tut: sie denkt nicht. Teardown und Rebuild schreibt Claude Code
in den Lauf-Ordner, hier liest du sie. Der Render startet erst nach deiner Freigabe,
und die Freigabe ist eine Datei (`approved.json`) im Lauf-Ordner, kein Zustand im
Browser.
"""
import argparse, json, mimetypes, os, pathlib, re, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
UI = ROOT / "scripts" / "ui"
FORMATS = ["ugc", "cinematic", "reaction", "mirror", "split"]
_procs = {}


def run_dirs():
    """Läufe aus runs/ plus die mitgelieferten Beispiele."""
    out = []
    for base in (ROOT / "runs", ROOT / "examples"):
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir(), reverse=True):
            if d.is_dir() and not d.name.startswith(".") and (d / "source.md").exists():
                out.append(d)
    return out


def find_run(run_id):
    for d in run_dirs():
        if d.name == run_id:
            return d
    return None


def read(p):
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def render_state(d):
    """render.json liegt je nach Route in raw/ oder direkt im Lauf."""
    for cand in (d / "raw" / "render.json", d / "render.json", d / "final" / "render.json"):
        j = load_json(cand)
        if j and j.get("jobs"):
            return j
    return None


def cost_total(d):
    """Die Summe aus cost.md. Nicht die erstbeste Zahl: das Guthaben steht dort auch."""
    txt = read(d / "cost.md")
    if not txt:
        return None
    # 1. Zeile, die nach Summe aussieht (Tabellenzeile oder Fliesstext)
    for line in txt.splitlines():
        if re.search(r"summe|gesamt|total", line, re.I):
            m = re.findall(r"([\d]+[.,][\d]{2})\s*\$", line)
            if m:
                return m[-1] + " $"
    # 2. fett ausgezeichneter Betrag
    m = re.findall(r"\*\*\s*([\d]+[.,][\d]{2})\s*\$\s*\*\*", txt)
    if m:
        return m[-1] + " $"
    # 3. grösster genannter Betrag, damit eine Teilsumme nicht als Gesamtpreis erscheint
    all_v = re.findall(r"([\d]+[.,][\d]{2})\s*\$", txt)
    if all_v:
        return max(all_v, key=lambda v: float(v.replace(",", "."))) + " $"
    return None


def media_files(d):
    """Fertige Clips: bevorzugt aus final/, sonst die Rohfassungen aus raw/."""
    out = []
    for unter in ("final", "raw"):
        ordner = d / unter
        if not ordner.is_dir():
            continue
        for f in sorted(ordner.iterdir()):
            if f.suffix.lower() not in (".mp4", ".mov", ".jpg", ".jpeg", ".png"):
                continue
            if f.stem.endswith(("-small", "-strip", "-poster")):
                continue
            name = f.stem.replace("-labeled", "").replace("-sheet", "")
            out.append({"format": name,
                        "kind": "video" if f.suffix.lower() in (".mp4", ".mov") else "sheet",
                        "url": f"/media/{d.name}/{unter}/{f.name}"})
        if out:
            break
    return out


def state(d):
    rs = render_state(d)
    jobs = (rs or {}).get("jobs", {})
    approved = load_json(d / "approved.json")
    if jobs and all(j.get("status") == "done" for j in jobs.values()):
        step = "fertig"
    elif jobs and any(j.get("status") in ("submitted", "queued") for j in jobs.values()):
        step = "rendert"
    elif approved:
        step = "freigegeben"
    elif (d / "rebuild.md").exists():
        step = "briefing"
    else:
        step = "teardown"
    return {
        "id": d.name,
        "beispiel": d.parent.name == "examples",
        "step": step,
        "source": read(d / "source.md"),
        "teardown": read(d / "teardown.md"),
        "rebuild": read(d / "rebuild.md") or read(d / "rebuild-pain.md"),
        "cost": read(d / "cost.md"),
        "cost_total": cost_total(d),
        "approved": approved,
        "jobs": {k: {kk: v[kk] for kk in ("status", "seconds", "result_url", "error") if kk in v}
                 for k, v in jobs.items()},
        "media": media_files(d),
        "has_prompts": (d / "prompts.json").exists(),
        "running": d.name in _procs and _procs[d.name].poll() is None,
    }


MAX_UPLOAD = 300 * 1024 * 1024   # 300 MB, mehr braucht eine Ad nicht


def slugify(text, fallback="lauf"):
    t = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (t[:40] or fallback)


def neuer_lauf(marke, link, notiz):
    """Legt runs/<datum>-<slug>/ mit source.md an. Mehr nicht: das Denken macht Claude Code."""
    marke = (marke or "").strip()
    link = (link or "").strip()
    notiz = (notiz or "").strip()
    if not (link or notiz):
        return None, "Gib einen Link zur Ad an oder füg das Transkript ein."
    ad_id = ""
    m = re.search(r"[?&]id=(\d+)", link)
    if m:
        ad_id = m.group(1)
    slug = slugify(marke or "lauf") + ("-" + ad_id[-6:] if ad_id else "")
    base = ROOT / "runs" / f"{time.strftime('%Y-%m-%d')}-{slug}"
    n = 2
    while base.exists():
        base = base.with_name(f"{base.name.rsplit('-', 1)[0] if n > 2 else base.name}-{n}")
        n += 1
    base.mkdir(parents=True)
    zeilen = ["# Quelle", ""]
    if marke:
        zeilen += [f"**Marke:** {marke}", ""]
    if link:
        zeilen += [f"**Wettbewerber-Ad:** {link}", ""]
    if ad_id:
        zeilen += [f"Bibliotheks-ID: {ad_id}", ""]
    zeilen += [f"Angelegt am {time.strftime('%d.%m.%Y um %H:%M')} über das Cockpit.", ""]
    if notiz:
        zeilen += ["## Transkript und Notizen", "", notiz, ""]
    (base / "source.md").write_text("\n".join(zeilen), encoding="utf-8")
    return base, None


def start_render(d):
    """Startet render-fal.py als Unterprozess. Nur nach Freigabe, nur einmal."""
    if not (d / "approved.json").exists():
        return False, "Nicht freigegeben."
    if not (d / "prompts.json").exists():
        return False, "prompts.json fehlt. Claude Code schreibt sie im Schritt /render."
    if d.name in _procs and _procs[d.name].poll() is None:
        return False, "Läuft bereits."
    out = d / "raw"
    out.mkdir(exist_ok=True)
    log = open(d / "render.log", "ab")
    _procs[d.name] = subprocess.Popen(
        [sys.executable, str(ROOT / "scripts" / "render-fal.py"), str(d / "prompts.json"), str(out)],
        stdout=log, stderr=log, cwd=str(ROOT))
    return True, "Render gestartet."


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path in ("/", "/index.html"):
            return self._send(200, read(UI / "index.html"), "text/html; charset=utf-8")
        if path == "/cockpit.css":
            return self._send(200, read(UI / "cockpit.css"), "text/css; charset=utf-8")
        if path == "/api/runs":
            return self._send(200, [{"id": d.name, "beispiel": d.parent.name == "examples",
                                     "step": state(d)["step"]} for d in run_dirs()])
        m = re.fullmatch(r"/api/run/([^/]+)", path)
        if m:
            d = find_run(m.group(1))
            return self._send(200, state(d)) if d else self._send(404, {"error": "unbekannter Lauf"})
        m = re.fullmatch(r"/media/([^/]+)/(.+)", path)
        if m:
            d = find_run(m.group(1))
            if not d:
                return self._send(404, {"error": "unbekannter Lauf"})
            f = (d / m.group(2)).resolve()
            if not str(f).startswith(str(d.resolve())) or not f.is_file():
                return self._send(404, {"error": "nicht gefunden"})
            ctype = mimetypes.guess_type(str(f))[0] or "application/octet-stream"
            data = f.read_bytes()
            return self._send(200, data, ctype, {"Accept-Ranges": "none"})
        self._send(404, {"error": "nicht gefunden"})

    def _body(self, limit):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return None
        if n <= 0 or n > limit:
            return None
        return self.rfile.read(n)

    def do_PUT(self):
        """Datei in einen Lauf legen. Rohe Bytes im Rumpf, Name im Kopf X-Dateiname."""
        path = unquote(urlparse(self.path).path)
        m = re.fullmatch(r"/api/run/([^/]+)/asset", path)
        if not m:
            return self._send(404, {"error": "nicht gefunden"})
        d = find_run(m.group(1))
        if not d:
            return self._send(404, {"error": "unbekannter Lauf"})
        if d.parent.name == "examples":
            return self._send(400, {"error": "Beispiel-Läufe sind schreibgeschützt."})
        name = pathlib.Path(unquote(self.headers.get("X-Dateiname") or "datei")).name
        name = re.sub(r"[^A-Za-z0-9._-]", "_", name)[:80] or "datei"
        data = self._body(MAX_UPLOAD)
        if data is None:
            return self._send(400, {"error": f"Datei fehlt oder ist größer als {MAX_UPLOAD // 1024 // 1024} MB."})
        (d / name).write_bytes(data)
        with (d / "source.md").open("a", encoding="utf-8") as f:
            f.write(f"\nMitgegeben: `{name}` ({len(data) // 1024} KB), liegt im Lauf-Ordner.\n")
        return self._send(200, {"ok": True, "datei": name, "bytes": len(data)})

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        if path == "/api/new":
            raw = self._body(64 * 1024)
            try:
                payload = json.loads(raw or b"{}")
            except Exception:
                return self._send(400, {"error": "ungültige Anfrage"})
            d, err = neuer_lauf(payload.get("marke"), payload.get("link"), payload.get("notiz"))
            if err:
                return self._send(400, {"error": err})
            return self._send(200, {"id": d.name})
        m = re.fullmatch(r"/api/run/([^/]+)/(approve|render)", path)
        if not m:
            return self._send(404, {"error": "nicht gefunden"})
        d = find_run(m.group(1))
        if not d:
            return self._send(404, {"error": "unbekannter Lauf"})
        if d.parent.name == "examples":
            return self._send(400, {"error": "Beispiel-Läufe sind schreibgeschützt. Leg einen eigenen Lauf unter runs/ an."})
        if m.group(2) == "approve":
            (d / "approved.json").write_text(json.dumps(
                {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "kosten": cost_total(d)},
                ensure_ascii=False, indent=1), encoding="utf-8")
            return self._send(200, state(d))
        ok, msg = start_render(d)
        return self._send(200 if ok else 400, {"ok": ok, "msg": msg})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=7788)
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"Cockpit läuft: http://127.0.0.1:{a.port}   (Strg+C beendet es)")
    print(f"Läufe: {', '.join(d.name for d in run_dirs()) or 'noch keine'}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nbeendet")


if __name__ == "__main__":
    main()
