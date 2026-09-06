#!/usr/bin/env python3
"""Wöchentliche Pflege der Ad-Bibliothek.

Verschiebt Einträge, die älter als 90 Tage sind, aus
brand/<marke>/ad_library_last_90_days.md in brand/<marke>/ad_library_archive.md,
dort verdichtet auf eine Zeile (Datum, Slug, Hook, Mechanik, ROAS).

    python3 scripts/rotate-library.py <marke> [--days 90] [--dry-run]

Einträge müssen mit einer Zeile "### YYYY-MM-DD · slug" beginnen.
"""
import re, sys, datetime, pathlib

def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__); sys.exit(1)
    brand = args[0]
    days = 90
    dry = "--dry-run" in args
    if "--days" in args:
        days = int(args[args.index("--days") + 1])
    root = pathlib.Path(__file__).resolve().parent.parent / "brand" / brand
    src = root / "ad_library_last_90_days.md"
    dst = root / "ad_library_archive.md"
    if not src.exists():
        print(f"nicht gefunden: {src}"); sys.exit(1)

    text = src.read_text(encoding="utf-8")
    head_re = re.compile(r"^### (\d{4}-\d{2}-\d{2}) · (.+)$", re.M)
    heads = list(head_re.finditer(text))
    if not heads:
        print("keine Einträge im Format '### YYYY-MM-DD · slug' gefunden"); return

    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    keep, move = [], []
    prefix = text[:heads[0].start()]
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[m.start():end]
        date = datetime.date.fromisoformat(m.group(1))
        (move if date < cutoff else keep).append((date, m.group(2).strip(), block))

    def field(block, name):
        mm = re.search(rf"^- {name}:\s*(.*)$", block, re.M)
        return mm.group(1).strip() if mm else ""

    lines = []
    for date, slug, block in move:
        lines.append(f"- {date} · {slug} · Hook: {field(block,'Hook')} · Mechanik: {field(block,'Mechanik')} · ROAS: {field(block,'ROAS')}")

    print(f"{len(keep)} bleiben, {len(move)} älter als {days} Tage")
    for l in lines: print("  " + l)
    if dry or not move:
        return

    src.write_text(prefix + "".join(b for _, _, b in keep), encoding="utf-8")
    header = "" if dst.exists() else "# Ad-Archiv (verdichtet)\n\nEine Zeile pro Ad, älter als 90 Tage. Rotiert von scripts/rotate-library.py.\n\n"
    with dst.open("a", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")
    print(f"geschrieben: {dst.name}")

if __name__ == "__main__":
    main()
