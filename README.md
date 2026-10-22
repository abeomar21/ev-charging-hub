# EV Charging Hub — Design Package

[![CI](https://github.com/abeomar21/ev-charging-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/abeomar21/ev-charging-hub/actions/workflows/ci.yml)

A self-initiated design study for a public EV charging hub at an assumed
commercial site in Greater Cairo: **2 × 22 kW AC + 2 × 60 kW DC (CCS2)**,
designed the way a junior design engineer at a charge-point operator would,
plus an **OCPP 1.6J simulator** that runs the same four chargers against an
open-source backend (SteVe).

Nobody built this hub. Every number traces to a standard clause, a datasheet,
a tariff page or a written assumption in [`assumptions.csv`](assumptions.csv).

## Status

| Phase | Scope | Status |
|---|---|---|
| P0 | Foundations: repo, CI, three-phase refresher, EV charging basics, standards map | In progress |
| P1 | Requirements: charter, site, chargers (DEC-02), demand assumptions | Not started |
| P2 | Load and load management (DEC-01, DEC-03), harmonics | Not started |
| P3 | SLD, cables, voltage drop, fault levels, protection (DEC-04), earthing | Not started |
| P4 | OCPP 1.6J simulator, fault injection, smart charging under the site cap | Not started |
| P5 | BoQ, CAPEX, revenue and feasibility | Not started |
| P6 | Commissioning, external review, final report, v1.0 release | Not started |

Five tasks ship in a lighter form; see [ROADMAP.md](ROADMAP.md#lite-scope).

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | Design notes, decisions (DEC-xx) and the learning log |
| `calcs/` | Python calculations: load, sessions, cables, fault levels, economics |
| `sld/` | Single-line diagram (draw.io source + PDF) |
| `boq/` | Bill of quantities and CAPEX estimate |
| `ocpp-sim/` | OCPP 1.6J charge-point simulator and SteVe setup |
| `references/` | Standards map (titles and clauses only, no paid PDFs) and datasheet notes |
| `scripts/` | Repo tooling, e.g. GitHub labels, milestones and issues bootstrap |
| `.github/` | CI workflows and issue templates |
| `assumptions.csv` | Assumptions register: every input with its source or a TO VERIFY flag |

## Getting started

```bash
python -m venv .venv
```

Setup, calculation and simulator instructions land here as each phase ships.
