#!/usr/bin/env python3
"""Render-Route fal.ai (statt Higgsfield-MCP). Stdlib only.

    python3 scripts/render-fal.py runs/<id>/prompts.json runs/<id>/final

Der Key kommt aus der .env im Repo oder aus der Umgebungsvariable FAL_KEY.

prompts.json: Liste von {name, endpoint, input}. Alle Jobs werden parallel
eingereicht, gepollt, die Ergebnisse als <name>.mp4 gespeichert und in
render.json protokolliert (request_id, result_url, Dauer, Fehler).
"""
import sys, os, json, time, threading, urllib.request, pathlib

def _fal_key():
    """FAL_KEY aus der Umgebung oder aus der .env im Repo-Wurzelverzeichnis."""
    key = os.environ.get("FAL_KEY")
    if key:
        return key.strip()
    env = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        found = None
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or not line.startswith("FAL_KEY="):
                continue
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            if value:            # leere Vorlagenzeile überspringen, letzte Zuweisung gewinnt
                found = value
        return found
    return None

KEY = _fal_key()
if not KEY:
    sys.exit("FAL_KEY fehlt. Trag ihn in die .env im Repo ein (Vorlage: .env.example) "
             "oder setz ihn als Umgebungsvariable. Key holen: fal.ai/dashboard/keys")
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
jobs = json.load(open(src))
state = {j["name"]: {"status": "queued"} for j in jobs}
lock = threading.Lock()

def call(url, data=None):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None)
    r.add_header("Authorization", "Key " + KEY); r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read())

def save():
    with lock:
        json.dump({"jobs": state, "updated": time.strftime("%Y-%m-%d %H:%M:%S")}, open(out / "render.json", "w"), indent=1, ensure_ascii=False)

def run(job):
    name, ep = job["name"], job["endpoint"]; t0 = time.time()
    try:
        sub = call(f"https://queue.fal.run/{ep}", job["input"])
        rid = sub["request_id"]
        with lock: state[name].update(status="submitted", request_id=rid)
        save()
        while True:
            st = call(sub["status_url"])
            s = st.get("status")
            if s == "COMPLETED": break
            if s in ("FAILED", "ERROR"):
                raise RuntimeError(json.dumps(st)[:500])
            time.sleep(5)
        res = call(sub["response_url"])
        url = (res.get("video") or {}).get("url") or res.get("video_url")
        path = out / f"{name}.mp4"
        urllib.request.urlretrieve(url, path)
        with lock: state[name].update(status="done", result_url=url, file=str(path), seconds=round(time.time() - t0), response=res)
    except Exception as e:
        with lock: state[name].update(status="failed", error=str(e)[:800], seconds=round(time.time() - t0))
    save()
    print(f"[{name}] {state[name]['status']} nach {state[name].get('seconds')}s", flush=True)

threads = [threading.Thread(target=run, args=(j,)) for j in jobs]
for t in threads: t.start()
for t in threads: t.join()
done = sum(1 for v in state.values() if v["status"] == "done")
print(f"{done}/{len(jobs)} fertig, Protokoll: {out/'render.json'}")
