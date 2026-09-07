#!/usr/bin/env python3
"""Lädt eine lokale Datei in den fal-Storage und gibt die öffentliche URL aus (stdlib only).
    python3 scripts/fal-upload.py clip.mp4

Der Key kommt aus der .env im Repo oder aus der Umgebungsvariable FAL_KEY.
"""
import sys, os, json, mimetypes, pathlib, urllib.request

def _fal_key():
    """FAL_KEY aus der Umgebung oder aus der .env im Repo-Wurzelverzeichnis."""
    key = os.environ.get("FAL_KEY")
    if key:
        return key.strip()
    env = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("FAL_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

key = _fal_key()
if not key:
    sys.exit("FAL_KEY fehlt. Trag ihn in die .env im Repo ein (Vorlage: .env.example).")
path = sys.argv[1]
ctype=mimetypes.guess_type(path)[0] or "application/octet-stream"
req=urllib.request.Request("https://rest.alpha.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3",
    data=json.dumps({"content_type":ctype,"file_name":os.path.basename(path)}).encode(), method="POST")
req.add_header("Authorization","Key "+key); req.add_header("Content-Type","application/json")
with urllib.request.urlopen(req,timeout=60) as r: init=json.loads(r.read())
data=open(path,"rb").read()
up=urllib.request.Request(init["upload_url"], data=data, method="PUT"); up.add_header("Content-Type",ctype)
with urllib.request.urlopen(up,timeout=300) as r: r.read()
print(init["file_url"])
