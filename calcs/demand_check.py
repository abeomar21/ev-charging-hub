"""Derive the DERIVED demand rows so no derived number is typed by hand.

Inputs (all through the register): A04b, A05b, A09, A11 (fleet_mix.csv),
A14 (arrival_profile.csv), A18.
Owns: A15, A16, A17 (values), and checks A11 shares and the A14 shape.

    python calcs/demand_check.py           # print the derivation
    python calcs/demand_check.py --write   # also write A15-A17 into assumptions.csv
"""
import csv
import sys

from assumptions import bounds, get, set_value

NUMERIC = ("jul2026_licences", "share", "usable_kwh", "ac_accept_kw", "dc_avg_kw", "soc_start", "soc_end")
OWNED = ("A15", "A16", "A17")  # rows this script writes, rounded to whole units


def load_fleet():
    with open(get("A11"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in NUMERIC:
            r[k] = float(r[k])
    assert abs(sum(r["share"] for r in rows) - 1.0) < 1e-9, "fleet shares must sum to 1"
    total = sum(r["jul2026_licences"] for r in rows)
    for r in rows:  # each rounded share must match the licensing data within 1 point
        assert abs(r["share"] - r["jul2026_licences"] / total) < 0.01, r["vehicle_class"]
    return rows, total


def load_profile():
    with open(get("A14"), newline="", encoding="utf-8") as f:
        prof = list(csv.DictReader(f))
    assert len(prof) == 24, "arrival profile needs 24 hours"
    return prof


def derive():
    """Return the derived values and the per-class breakdown."""
    fleet, total = load_fleet()
    p_dc, p_ac = get("A05b"), get("A04b")
    overhead, ac_dwell = get("A09"), get("A18")

    classes, e_dc, t_dc = [], 0.0, 0.0
    for r in fleet:
        energy = r["usable_kwh"] * (r["soc_end"] - r["soc_start"])
        p_eff = min(r["dc_avg_kw"], p_dc)
        minutes = energy / p_eff * 60 + overhead
        e_dc += r["share"] * energy
        t_dc += r["share"] * minutes
        classes.append((r["vehicle_class"], r["share"], energy, p_eff, minutes))

    ac_draw = sum(r["share"] * min(r["ac_accept_kw"], p_ac) for r in fleet)
    return {
        "licences": total,
        "classes": classes,
        "A15": e_dc,
        "A16": ac_draw * ac_dwell / 60,
        "A17": t_dc,
        "ac_draw_kw": ac_draw,
    }


def main(write=False):
    d = derive()
    print(f"A11 fleet mix from {d['licences']:.0f} July 2026 licences (top-10 brands)")
    for name, share, energy, p_eff, minutes in d["classes"]:
        print(f"  {name:<10} {share:4.0%}  {energy:5.1f} kWh  {p_eff:5.1f} kW  {minutes:5.1f} min")
    print(f"A15 weighted DC session energy: {d['A15']:.1f} kWh")
    print(f"A17 weighted DC dwell:          {d['A17']:.1f} min")
    print(f"A19 weighted AC draw per {get('A04b'):.0f} kW point: {d['ac_draw_kw']:.1f} kW")
    print(f"A16 AC energy at {get('A18'):.0f} min dwell:  {d['A16']:.1f} kWh")

    for col in ("dc_weight", "ac_weight"):
        w = [float(p[col]) for p in load_profile()]
        s = sum(w)
        peak = max(w)
        peaks = [h for h in range(24) if w[h] == peak]
        print(f"A14 {col}: peak {peaks[0]:02d}:00-{peaks[-1] + 1:02d}:00, "
              f"07:00-23:00 share {sum(w[7:23]) / s:.0%}")

    for label, n in zip(("low", "base", "high"), bounds("A12")):
        print(f"A12 {label:<4} {n:g} DC sessions/day -> {n * d['A15']:4.0f} kWh/day/point, "
              f"time-utilisation {n * d['A17'] / 1440:.0%}")

    if write:
        for aid in OWNED:
            set_value(aid, f"{d[aid]:.0f}")
        print("wrote " + ", ".join(f"{a}={d[a]:.0f}" for a in OWNED) + " to assumptions.csv")


if __name__ == "__main__":
    main(write="--write" in sys.argv)
