"""The assumptions register: the one place design inputs live.

Every script reads its inputs through get() instead of hard-coding them:

    from assumptions import get
    p_dc = get("A05b")          # 60.0 (kW)
    fleet = get("A11")          # Path to calcs/data/fleet_mix.csv

Run it directly to check the register and regenerate the readable table:

    python calcs/assumptions.py        # exits 1 if any row breaks a rule
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "assumptions.csv"
TABLE_DOC = ROOT / "docs" / "assumptions-register.md"

COLUMNS = ["id", "parameter", "kind", "value", "unit", "low", "high", "distribution",
           "source", "status", "confidence", "verify", "used_by", "notes"]
KINDS = {"number", "text", "file"}
STATUSES = {
    "SOURCED": "taken from a datasheet, standard, tariff or published data",
    "DERIVED": "calculated by a script named in the source column",
    "DECIDED": "fixed by a decision record, the charter or the site choice",
    "ASSUMED": "engineering judgement; the reasoning is in the notes",
    "TO VERIFY": "best available value, still needs checking",
}
CONFIDENCE = ("High", "Medium", "Low")
ID_RE = re.compile(r"^A(\d{2})([a-z]?)$")
SOURCE_MARKERS = ("http", "www.", ".com", ".org", ".gov", "IEC", "datasheet", "references/")


def load(path=REGISTER):
    """Return the register as {id: row} in file order."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise ValueError(f"columns must be {COLUMNS}, got {reader.fieldnames}")
        rows = {}
        for r in reader:
            if None in r:
                raise ValueError(f"{r['id']}: too many fields (unquoted comma?)")
            if r["id"] in rows:
                raise ValueError(f"duplicate id {r['id']}")
            rows[r["id"]] = r
    return rows


def get(aid, path=REGISTER):
    """Value of one assumption: float for numbers, Path for files, str for text."""
    r = load(path)[aid]
    if r["kind"] == "number":
        return float(r["value"])
    if r["kind"] == "file":
        return ROOT / r["value"]
    return r["value"]


def bounds(aid, path=REGISTER):
    """(low, value, high) for a number row; missing bounds fall back to the value."""
    r = load(path)[aid]
    v = float(r["value"])
    lo = float(r["low"]) if r["low"] else v
    hi = float(r["high"]) if r["high"] else v
    return lo, v, hi


def set_value(aid, value, path=REGISTER):
    """Rewrite one value in the register. Used by scripts that own DERIVED rows."""
    rows = load(path)
    rows[aid]["value"] = value
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows.values())


def validate(rows):
    """Return a list of rule breaks. An empty list means the register is clean."""
    problems = []
    seen_numbers = set()
    for aid, r in rows.items():
        m = ID_RE.match(aid)
        if not m:
            problems.append(f"{aid}: id must look like A01 or A04a")
            continue
        seen_numbers.add(int(m.group(1)))
        say = lambda msg: problems.append(f"{aid}: {msg}")

        for col in ("parameter", "value", "source", "used_by"):
            if not r[col].strip():
                say(f"{col} is empty")
        if r["kind"] not in KINDS:
            say(f"kind '{r['kind']}' not in {sorted(KINDS)}")
        if r["status"] not in STATUSES:
            say(f"status '{r['status']}' not in {list(STATUSES)}")
        if r["confidence"] not in CONFIDENCE:
            say(f"confidence '{r['confidence']}' not in {CONFIDENCE}")

        if r["kind"] == "number":
            try:
                v = float(r["value"])
            except ValueError:
                say(f"value '{r['value']}' is not a number")
                continue
            if not r["unit"].strip():
                say("number without a unit")
            lo = float(r["low"]) if r["low"] else v
            hi = float(r["high"]) if r["high"] else v
            if not lo <= v <= hi:
                say(f"value {v} outside low/high {lo}-{hi}")
        elif r["kind"] == "file" and not (ROOT / r["value"]).exists():
            say(f"file {r['value']} does not exist")

        src = r["source"]
        if r["status"] == "SOURCED" and not any(k in src for k in SOURCE_MARKERS):
            say("SOURCED but the source names no link, standard or datasheet")
        if r["status"] == "DERIVED":
            scripts = re.findall(r"calcs/\w+\.py", src)
            if not scripts:
                say("DERIVED but the source names no calcs/*.py script")
            for s in scripts:
                if not (ROOT / s).exists():
                    say(f"script {s} does not exist")
        if r["status"] == "DECIDED" and not any(k in src for k in ("DEC-", "docs/", "references/")):
            say("DECIDED but the source names no decision record or doc")
        if r["status"] == "ASSUMED" and not r["notes"].strip():
            say("ASSUMED without reasoning in notes")
        if (r["status"] == "TO VERIFY" or r["confidence"] == "Low") and not r["verify"].strip():
            say("flagged but the verify column says nothing about how to check it")

    expected = set(range(1, max(seen_numbers, default=0) + 1))
    for n in sorted(expected - seen_numbers):
        problems.append(f"A{n:02d}: missing (numbering gap)")
    return problems


def _md(text):
    return text.replace("|", "/").replace("\n", " ")


def write_table(rows, path=TABLE_DOC):
    """Generate docs/assumptions-register.md from the CSV. Never edit that file by hand."""
    status = Counter(r["status"] for r in rows.values())
    conf = Counter(r["confidence"] for r in rows.values())
    lines = [
        "# Assumptions register",
        "",
        "Generated by `python calcs/assumptions.py` from `assumptions.csv`. Do not edit by hand.",
        "",
        f"**{len(rows)} rows.** "
        + ", ".join(f"{status[s]} {s}" for s in STATUSES if status[s])
        + ". Confidence: " + ", ".join(f"{conf[c]} {c}" for c in CONFIDENCE if conf[c]) + ".",
        "",
        "| Status | Meaning |",
        "|---|---|",
        *[f"| {s} | {m} |" for s, m in STATUSES.items()],
        "",
        "## All rows",
        "",
        "| ID | Parameter | Value | Range | Status | Confidence | Used by |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows.values():
        if r["kind"] == "file":
            value = f"`{r['value']}`"
        else:
            value = f"{r['value']} {r['unit'] if r['unit'] != '-' else ''}".strip()
        rng = f"{r['low']}-{r['high']}" if r["low"] and r["high"] else ""
        lines.append(f"| {r['id']} | {_md(r['parameter'])} | {_md(value)} | {rng} | "
                     f"{r['status']} | {r['confidence']} | {_md(r['used_by'])} |")
    lines += ["", "## Still open", "",
              "Rows marked TO VERIFY or Low confidence, and what would firm them up.", "",
              "| ID | Parameter | How to check it |", "|---|---|---|"]
    for r in rows.values():
        if r["status"] == "TO VERIFY" or r["confidence"] == "Low":
            lines.append(f"| {r['id']} | {_md(r['parameter'])} | {_md(r['verify'])} |")
    lines += ["", "Sources, notes and distributions for every row are in `assumptions.csv`.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    rows = load()
    problems = validate(rows)
    write_table(rows)
    status = Counter(r["status"] for r in rows.values())
    print(f"{len(rows)} rows: " + ", ".join(f"{n} {s}" for s, n in status.items()))
    print(f"wrote {TABLE_DOC.relative_to(ROOT)}")
    for p in problems:
        print("PROBLEM", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
