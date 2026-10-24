# 01 — Project Charter

| | |
|---|---|
| **Project** | EV Charging Hub Design Package (`ev-charging-hub`) |
| **Task** | T1.1 · Phase P1 — Requirements, site and equipment |
| **Author** | Abdelrahman Hany |
| **Status** | Rev A — draft for v0.1 |
| **Related** | [`assumptions.csv`](../assumptions.csv) · [`00-background.md`](00-background.md) · [`02-site.md`](02-site.md) · [`ROADMAP.md`](../ROADMAP.md) |

---

## 1. Purpose

Produce, on paper and in code, the design package for a public EV charging hub with **2 AC and 2 DC charge points** at a commercial site in Greater Cairo, to the depth a junior design engineer at a charge-point operator (CPO) or EPC contractor would deliver it.

The package has two halves joined by one test:

1. **Electrical design** — load study with load management, single-line diagram, cable / voltage-drop / fault-level / protection / earthing calculations, priced BoQ, feasibility and a commissioning checklist.
2. **OCPP 1.6J simulator** — four simulated charge points running against an open-source central system (SteVe).
3. **The joint** — the site power cap calculated in the load study (T2.4) is pushed by the backend as a charging profile and honoured by the simulator (T4.6).

## 2. Framing

This is a **self-initiated design study**. Nothing will be built, no client has commissioned it, and no site has been surveyed. Its value is traceability: every number in the package must point to a standard clause, a datasheet, a tariff page or an assumption ID in `assumptions.csv`. A number that cannot be traced does not go in.

## 3. Design basis (summary)

The full, sourced list lives in `assumptions.csv`. The charter only names the assumptions that set scope.

| ID | Assumption | Scope effect |
|---|---|---|
| A01 | Commercial site in Greater Cairo (mall car park or fuel station) | Assumed site; see §5 exclusions |
| A02 | 400/230 V, 3-phase + N, 50 Hz, TN-S inside the site | LV design only |
| A03 | IEC 60364 (Part 7-722), IEC 61851, IEC 62196, EgyptERA EV rules | Code basis for every check |
| A04 | 2 × 22 kW AC, Type 2 | AC feeders and protection |
| A05 | 2 × 60 kW DC, CCS2 (baseline) | Compared against 2 × 120 kW in DEC-01 |
| A06 | Auxiliary loads (placeholder) | Aux board on the SLD |
| A07 | 40 °C air / 30 °C ground design ambient | Cable derating |

## 4. Scope — in

| Area | Deliverable | Task(s) | Location |
|---|---|---|---|
| Foundations | Background explainer, standards map | T0.2–T0.4 | `docs/00-background.md`, `references/` |
| Requirements | Charter, site sketch, charger selection (DEC-02), demand assumptions | T1.1–T1.5 | `docs/01`–`02`, `docs/decisions/`, `assumptions.csv` |
| Load | Connected load, diversity argument, Monte Carlo session model, managed vs unmanaged peak, supply sizing (DEC-01, DEC-03), harmonics check | T2.1–T2.6 | `calcs/load.py`, `calcs/sessions.py`, `docs/03-load.md` |
| Electrical design | SLD rev A, cable schedule with derating and VD, fault levels, protection schedule (DEC-04), earthing note, adiabatic withstand | T3.1–T3.7 | `sld/`, `calcs/cables.py`, `docs/` |
| Simulator | SteVe running, 4 charge points, full transactions, 5 fault scenarios, site cap enforced, tests + CI, protocol doc | T4.1–T4.8 | `ocpp-sim/`, `docs/10-ocpp.md` |
| Cost | BoQ, Class 5 CAPEX estimate, revenue model, NPV / IRR / break-even, tornado | T5.1–T5.4 | `boq/`, `calcs/economics.py`, `docs/08-economics.md` |
| Close-out | IEC 60364-6 commissioning checklist, charger tests, external review, final report, v1.0 release | T6.1–T6.5 | `docs/09-commissioning.md`, `report/` |

## 5. Scope — out

Stated up front so a reviewer sees the boundary before looking for it.

- **Construction, procurement and site works.** No civil, canopy, structural, drainage or parking-layout design.
- **MV design.** The study stops at the LV side of the supply transformer; MV switchgear and utility connection are noted only as an option in DEC-03.
- **A real site.** The site is assumed and sketched (T1.2 ships *lite*); no survey, geotechnical or soil-resistivity data.
- **Utility approvals and permits.** EgyptERA and distribution-company procedures are cited, not executed.
- **Charger internals.** Chargers are treated as datasheet black boxes; no power-electronics design.
- **OCPP 2.0.1, ISO 15118 / Plug & Charge, payment and roaming (OCPI).** Parked in `ROADMAP.md` for v2.
- **Solar PV, battery storage, V2G.** Parked for v2.
- **Supplier quotes.** Prices are desk-sourced; the CAPEX is Class 5 (T5.2 ships *lite*).

## 6. Success criteria

v1.0 is done when every line below is true and checkable in the repo.

| # | Criterion | Evidence |
|---|---|---|
| S1 | Every numeric value in `docs/` and `report/` traces to a script output, a cited source or an assumption ID | Spot-check any 5 numbers; all trace |
| S2 | No assumption in `assumptions.csv` lacks a source or a `TO VERIFY` flag | CSV has no blank source/status cells |
| S3 | Load study reports unmanaged and managed site peak (kW) from ≥ 1,000 simulated days | `docs/03-load.md`, load duration curves |
| S4 | Every circuit on the SLD appears in the cable schedule with Iz, VD %, fault level and withstand pass/fail | `calcs/cables.py` output |
| S5 | Every design choice with real options has a decision record before the work that depends on it | `docs/decisions/DEC-01` … `DEC-04` |
| S6 | The simulator stays at or under the backend-imposed site cap for a replayed simulated day | Site-kW vs cap chart (T4.6) |
| S7 | Five fault scenarios documented with expected vs observed behaviour | `ocpp-sim/` results |
| S8 | CI is green on `main` | README badge |
| S9 | CAPEX states its estimate class and range; every price has a source and date | `boq/` priced file |
| S10 | At least one external reviewer's comments are logged as issues and closed, or the review is marked pending in the README | GitHub issues, README |
| S11 | Every *lite* task is labelled as such in README and ROADMAP | README "Status" table |
| S12 | v1.0 tagged with report and one-page summary attached to the release | GitHub release |

## 7. Constraints

- **Standards access.** IEC standards are paywalled. Methods are learned from free IEC-based guides (e.g. Schneider Electric Electrical Installation Guide); the standard is cited by title, edition and clause. **No standards PDFs are committed.**
- **Data.** Egyptian EV equipment prices and site data are not public; every such value is labelled with source, date or `TO VERIFY`.
- **Tools.** Python (numpy, pandas, matplotlib, pandapower, ocpp), draw.io, Docker + SteVe, GitHub Actions — all free / open source.

## 8. Stakeholders and roles

| Role | Who | Responsibility |
|---|---|---|
| Designer / owner | Abdelrahman Hany — mechatronics engineering graduate (coursework in Circuits, Power Engineering and Power Electronics) | All design, code and documentation; the learning log is a refresher record |
| External reviewer | _[name, role — TBC]_ | 30-minute review of SLD and cable schedule (T6.3) |
| Intended readers | Hiring engineers (power / e-mobility), peers | Verify any number back to its source |

## 9. Milestones

| Tag | Content |
|---|---|
| v0.1 | Repo, CI, background, standards map, charter, site, DEC-02, assumptions |
| v0.2 | Load study, session model, DEC-01, DEC-03, harmonics |
| v0.3 | SLD rev A, cable schedule, fault levels, protection, earthing; sent to reviewer |
| v0.4 | OCPP simulator, site cap enforced, fault scenarios, CI |
| v0.9 | OCPP doc, BoQ, economics, commissioning, review handled, README |
| **v1.0** | Final report, release, summary |

## 10. Top risks

| Risk | Mitigation |
|---|---|
| Untraceable numbers ("calc theatre") | Assumptions register; scripts write all tables and figures |
| Load study slips and blocks both P3 and P4 | P2 protected; cut line drops dynamic sharing, never the static cap |
| No reviewer reply in time | Mark T6.3 "external review pending" openly |
| Docker / SteVe setup eats a day | Fallback to the `ocpp` package example central system; T4.6 never cut |
| Overclaiming | Always described as a *self-initiated design study* |

## 11. Change control

Scope changes are logged as a GitHub issue labelled `scope` and, if they alter a design input, as a new row or revision in `assumptions.csv`. This charter is revised only at a tagged milestone (Rev A → Rev B).

---

| Rev | Change |
|---|---|
| A | First issue |
