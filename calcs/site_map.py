"""Overview map of the site screening for docs/02-site.md.

Plots candidate host sites, existing chargers and Electra sites from
calcs/data/site_points.csv on a local metric grid (km east/north of the
chosen site) and draws a 3 km screening ring around it.
Output: docs/img/02-site-overview.png
"""
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CHOSEN = "S1"
SHORTLIST = {"S1", "S3"}
RESERVE = {"S2"}
RING_KM = 3.0

# Reference palette (dataviz skill), first three categorical slots + neutrals
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#9a9893", "#e6e5e1", "#fcfcfb"

SHORT = {
    "S1": "Mobil Hadayek October (chosen)",
    "S2": "eni station",
    "S3": "TotalEnergies, Fayoum rd",
    "S4": "Al Hamd Mall",
    "S5": "Zewail Plaza",
    "S6": "October Club 2",
    "S7": "BETA Club",
    "S8": "Al Sharq station",
    "S9": "Mobil Gohaina Sq.",
    "S10": "Espana Plaza",
    "E1": "Electra West Park Mall",
    "E2": "Electra Galleria40",
}


def main():
    rows = list(csv.DictReader(open(ROOT / "calcs/data/site_points.csv", encoding="utf-8")))
    by = {r["id"]: r for r in rows}
    lat0, lon0 = float(by[CHOSEN]["lat"]), float(by[CHOSEN]["lon"])
    kx = 111.320 * math.cos(math.radians(lat0))
    ky = 110.574

    def xy(r):
        return (float(r["lon"]) - lon0) * kx, (float(r["lat"]) - lat0) * ky

    fig, ax = plt.subplots(figsize=(9, 9), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ring = plt.Circle((0, 0), RING_KM, fill=False, ls="--", lw=1.2, color=BLUE, alpha=0.7)
    ax.add_patch(ring)
    ax.text(0, -RING_KM - 0.35, f"{RING_KM:.0f} km screening ring", ha="center", va="top",
            fontsize=8, color=INK2)

    for r in rows:
        x, y = xy(r)
        rid, role = r["id"], r["role"]
        if role == "candidate" and rid in SHORTLIST:
            size = 220 if rid == CHOSEN else 110
            ax.scatter(x, y, s=size, marker="*" if rid == CHOSEN else "o", color=BLUE,
                       edgecolor=SURFACE, linewidth=1.5, zorder=5)
        elif role == "candidate" and rid in RESERVE:
            ax.scatter(x, y, s=110, marker="o", facecolor=SURFACE, edgecolor=BLUE, linewidth=2, zorder=5)
        elif role == "candidate":
            ax.scatter(x, y, s=70, marker="X", color=MUTED, edgecolor=SURFACE, linewidth=1, zorder=4)
        elif role in ("charger", "host-of-concern"):
            ax.scatter(x, y, s=80, marker="^", color=ORANGE, edgecolor=SURFACE, linewidth=1.2,
                       zorder=4, alpha=1 if role == "charger" else 0.55)
        elif role == "electra":
            ax.scatter(x, y, s=90, marker="s", color=AQUA, edgecolor=SURFACE, linewidth=1.2, zorder=4)
        if rid in SHORT:
            dx, dy, ha = 0.25, 0.18, "left"
            if rid == "S10":
                dx, ha = -0.25, "right"
            if rid == "E1":
                dx, dy, ha = 0, -0.75, "center"
            if rid == "S9":
                dx, dy = 0.25, 0.25
            if rid == "S5":
                dy = 0.35
            if rid == "S2":
                dx, ha, dy = -0.25, "right", 0.2
            ax.text(x + dx, y + dy, SHORT[rid], fontsize=8.5 if rid != CHOSEN else 9.5,
                    color=INK if rid in SHORTLIST | RESERVE or rid.startswith("E") else INK2,
                    fontweight="bold" if rid == CHOSEN else "normal", ha=ha, zorder=6)

    # legend (shape + colour, so identity is never colour alone)
    handles = [
        plt.Line2D([], [], marker="*", ls="", ms=13, color=BLUE, label="Chosen site"),
        plt.Line2D([], [], marker="o", ls="", ms=8, color=BLUE, label="Shortlisted alternative"),
        plt.Line2D([], [], marker="o", ls="", ms=8, markerfacecolor=SURFACE, markeredgecolor=BLUE,
                   markeredgewidth=2, label="Reserve (no separate lot)"),
        plt.Line2D([], [], marker="X", ls="", ms=8, color=MUTED, label="Rejected candidate"),
        plt.Line2D([], [], marker="^", ls="", ms=9, color=ORANGE, label="Existing charger (competitor / unknown)"),
        plt.Line2D([], [], marker="^", ls="", ms=9, color=ORANGE, alpha=0.55, label="Chillout station (hosts Infinity elsewhere)"),
        plt.Line2D([], [], marker="s", ls="", ms=8, color=AQUA, label="Electra site"),
    ]
    leg = ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.01, 0.62), fontsize=8.5, frameon=True)
    leg.get_frame().set_edgecolor(GRID)
    leg.get_frame().set_facecolor(SURFACE)

    ax.set_aspect("equal")
    ax.grid(color=GRID, lw=0.8)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.set_xlabel("km east of chosen site", color=INK2, fontsize=9)
    ax.set_ylabel("km north of chosen site", color=INK2, fontsize=9)
    ax.set_title("Site screening: south-west gateway (Hadayek October)", loc="left",
                 fontsize=12, color=INK, pad=12)
    fig.text(0.125, 0.035, "Positions from Google Maps listings read 26 Oct 2026 "
             "(calcs/data/site_points.csv). Listings are incomplete; not every charger is mapped.",
             fontsize=7.5, color=INK2)

    out = ROOT / "docs/img/02-site-overview.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor=SURFACE)
    print(out)


if __name__ == "__main__":
    main()
