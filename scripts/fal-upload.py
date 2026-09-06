#!/usr/bin/env python3
"""Lädt eine lokale Datei in den fal-Storage und gibt die öffentliche URL aus (stdlib only).
    FAL_KEY=… python3 scripts/fal-upload.py clip.mp4
"""
import sys, os, json, mimetypes, urllib.request
key=os.environ["FAL_KEY"]; path=sys.argv[1]
ctype=mimetypes.guess_type(path)[0] or "application/octet-stream"
req=urllib.request.Request("https://rest.alpha.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3",
    data=json.dumps({"content_type":ctype,"file_name":os.path.basename(path)}).encode(), method="POST")
req.add_header("Authorization","Key "+key); req.add_header("Content-Type","application/json")
with urllib.request.urlopen(req,timeout=60) as r: init=json.loads(r.read())
data=open(path,"rb").read()
up=urllib.request.Request(init["upload_url"], data=data, method="PUT"); up.add_header("Content-Type",ctype)
with urllib.request.urlopen(up,timeout=300) as r: r.read()
print(init["file_url"])
