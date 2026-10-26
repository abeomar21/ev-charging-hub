"""Site screening distances for docs/02-site.md.

Reads calcs/data/site_points.csv and writes, for every candidate site, the
distance to the nearest competitor charger and the nearest Electra site
(great-circle / haversine distance, km). Output: docs/tables/site_screen.csv
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R_EARTH_KM = 6371.0088  # IUGG mean Earth radius


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(math.sqrt(a))


def nearest(site, others):
    best = min(others, key=lambda o: haversine_km(site["lat"], site["lon"], o["lat"], o["lon"]))
    return best, haversine_km(site["lat"], site["lon"], best["lat"], best["lon"])


def main():
    rows = list(csv.DictReader(open(ROOT / "calcs/data/site_points.csv", encoding="utf-8")))
    for r in rows:
        r["lat"], r["lon"] = float(r["lat"]), float(r["lon"])
    cands = [r for r in rows if r["role"] == "candidate"]
    chargers = [r for r in rows if r["role"] == "charger"]
    electra = [r for r in rows if r["role"] == "electra"]

    out = ROOT / "docs/tables/site_screen.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "site", "nearest_charger", "charger_km", "nearest_electra", "electra_km"])
        for c in cands:
            ch, dch = nearest(c, chargers)
            el, del_ = nearest(c, electra)
            w.writerow([c["id"], c["name"], ch["name"], f"{dch:.1f}", el["name"], f"{del_:.1f}"])
            print(f"{c['id']:<4}{c['name'][:42]:<44}{ch['name'][:34]:<36}{dch:5.1f} km  {el['name'][:24]:<26}{del_:5.1f} km")

    # extra pairs quoted in the text
    by = {r["id"]: r for r in rows}
    for a, b in [("S1", "S3"), ("S1", "S2"), ("S2", "S9"), ("S8", "C9"), ("S6", "C1")]:
        d = haversine_km(by[a]["lat"], by[a]["lon"], by[b]["lat"], by[b]["lon"])
        print(f"{a}-{b}: {d:.1f} km")


if __name__ == "__main__":
    main()
