"""Derive the DERIVED rows of A10-A20 so no derived number is typed by hand.

Inputs : calcs/data/fleet_mix.csv, calcs/data/arrival_profile.csv
Outputs: printed values for A11 shares, A15, A16, A17, A19, and a check of A14.
Run    : python calcs/demand_check.py
"""
import csv
from pathlib import Path

DATA = Path(__file__).parent / "data"
DC_CHARGER_KW = 60.0      # A05
AC_POINT_KW = 22.0        # A04
PLUG_OVERHEAD_MIN = 5.0   # A17: plug in, authorise, unplug (assumption)
AC_DWELL_MEAN_MIN = 60.0  # A18 base
NUMERIC = ("jul2026_licences", "share", "usable_kwh", "ac_accept_kw", "dc_avg_kw", "soc_start", "soc_end")


def load_fleet():
    with open(DATA / "fleet_mix.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in NUMERIC:
            r[k] = float(r[k])
    assert abs(sum(r["share"] for r in rows) - 1.0) < 1e-9, "fleet shares must sum to 1"
    total = sum(r["jul2026_licences"] for r in rows)
    for r in rows:  # the rounded share must match the licensing data within 1 point
        assert abs(r["share"] - r["jul2026_licences"] / total) < 0.01, r["vehicle_class"]
    return rows, total


def main():
    fleet, total = load_fleet()
    print(f"A11 fleet mix from {total:.0f} July 2026 licences (top-10 brands)")

    e_dc = t_dc = 0.0
    for r in fleet:
        energy = r["usable_kwh"] * (r["soc_end"] - r["soc_start"])
        p_eff = min(r["dc_avg_kw"], DC_CHARGER_KW)
        minutes = energy / p_eff * 60 + PLUG_OVERHEAD_MIN
        e_dc += r["share"] * energy
        t_dc += r["share"] * minutes
        print(f"  {r['vehicle_class']:<10} {r['share']:4.0%}  {energy:5.1f} kWh  {p_eff:5.1f} kW  {minutes:5.1f} min")
    print(f"A15 weighted DC session energy: {e_dc:.1f} kWh")
    print(f"A17 weighted DC dwell:          {t_dc:.1f} min")

    p_ac = sum(r["share"] * min(r["ac_accept_kw"], AC_POINT_KW) for r in fleet)
    print(f"A19 weighted AC draw per 22 kW point: {p_ac:.1f} kW")
    print(f"A16 AC energy at {AC_DWELL_MEAN_MIN:.0f} min dwell:  {p_ac * AC_DWELL_MEAN_MIN / 60:.1f} kWh")

    with open(DATA / "arrival_profile.csv", newline="") as f:
        prof = list(csv.DictReader(f))
    assert len(prof) == 24
    for col in ("dc_weight", "ac_weight"):
        w = [float(p[col]) for p in prof]
        s = sum(w)
        peak_h = max(range(24), key=lambda h: w[h])
        print(f"A14 {col}: peak hour {peak_h:02d}:00 ({w[peak_h] / s:.1%} of the day), 07-22 share {sum(w[7:23]) / s:.0%}")

    for label, n in (("low", 2), ("base", 4), ("high", 7)):
        print(f"A12 {label:<4} {n} DC sessions/day -> {n * e_dc:5.0f} kWh/day/point, "
              f"time-utilisation {n * t_dc / 1440:.0%}")


if __name__ == "__main__":
    main()
