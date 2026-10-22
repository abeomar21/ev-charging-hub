# Roadmap

Six-day sprint, 22–27 Oct 2026, about 60 hours. All 40 tasks from the
original plan are kept: 35 ship in full and 5 ship lite, labelled below.

## Milestones

| Day | Date | Theme | Phase | Gate |
|---|---|---|---|---|
| 1 | Thu 22 Oct | Foundations and requirements | P0 + P1 | Repo with green CI, 40 issues on the board, background, standards map, charter, site sketch, DEC-02, assumptions A01–A20. Tag **v0.1** |
| 2 | Fri 23 Oct | Load and load management | P2 | `load.py`, `sessions.py`, load duration curves, DEC-01, DEC-03, harmonics note. Tag **v0.2** |
| 3 | Sat 24 Oct | SLD, cables and protection | P3 | SLD rev A, cable schedule with VD, fault level and withstand columns, protection schedule, DEC-04, earthing note. Sent to reviewer |
| 4 | Sun 25 Oct | OCPP 1.6J simulator | P4 | Simulator replays a day, site-cap chart, 5 fault results, green CI. Tag **v0.4** |
| 5 | Mon 26 Oct | Money, commissioning and review | P4 docs + P5 + P6 | OCPP doc, priced BoQ, economics and tornado, commissioning checklist, review issues handled, README. Tag **v0.9** |
| 6 | Tue 27 Oct | Release | P6 | v1.0 release live with the report attached |

## Tasks

| ID | Task | Day | Ships as |
|---|---|---|---|
| T0.1 | Repo, issues and Projects board | 1 | Full |
| T0.2 | Three-phase power refresher | 1 | Full |
| T0.3 | How EV charging works | 1 | Full |
| T0.4 | Standards and regulations map | 1 | Full |
| T0.5 | Python environment and CI | 1 | Full |
| T1.1 | Project charter | 1 | Full |
| T1.2 | Site assessment | 1 | Lite |
| T1.3 | Pick real chargers (DEC-02) | 1 | Full |
| T1.4 | Demand assumptions A10–A20 | 1 | Full |
| T1.5 | Assumptions register | 1 | Full |
| T2.1 | Connected-load calculation | 2 | Full |
| T2.2 | Diversity and demand factor | 2 | Full |
| T2.3 | Session simulator | 2 | Full |
| T2.4 | Unmanaged vs managed demand | 2 | Full |
| T2.5 | Size the supply (DEC-03) | 2 | Full |
| T2.6 | Harmonics check | 2 | Full |
| T3.1 | Single-line diagram, rev A | 3 | Full |
| T3.2 | Cable sizing by current | 3 | Full |
| T3.3 | Voltage drop | 3 | Full |
| T3.4 | Short-circuit levels | 3 | Full |
| T3.5 | Protective devices (DEC-04) | 3 | Full |
| T3.6 | Earthing and bonding | 3 | Lite |
| T3.7 | Cable short-circuit withstand | 3 | Full |
| T4.1 | Run SteVe locally | 4 | Full |
| T4.2 | First connection | 4 | Full |
| T4.3 | Full transaction | 4 | Full |
| T4.4 | Model the hub | 4 | Full |
| T4.5 | Fault injection, 5 scenarios | 4 | Full |
| T4.6 | Smart charging under the site cap | 4 | Full |
| T4.7 | Tests and CI | 4 | Full |
| T4.8 | Document the protocol | 5 | Full |
| T5.1 | Bill of quantities | 5 | Full |
| T5.2 | CAPEX estimate | 5 | Lite |
| T5.3 | Revenue model | 5 | Full |
| T5.4 | Feasibility metrics and tornado | 5 | Full |
| T6.1 | Commissioning checklist | 5 | Full |
| T6.2 | Charger-level tests | 5 | Full |
| T6.3 | External design review | 5 | Lite |
| T6.4 | Final report | 6 | Lite |
| T6.5 | Release v1.0 and summary | 6 | Full |

## Lite scope

| ID | Task | What "lite" means |
|---|---|---|
| T1.2 | Site assessment | Assumed site and a sketch with distances; no site visit |
| T3.6 | Earthing and bonding | Earthing note and one disconnection-time check, not every circuit |
| T5.2 | CAPEX estimate | Class 5 from desk prices; Class 4 needs supplier quotes |
| T6.3 | External design review | One reviewer, weekend turnaround; marked pending if no reply |
| T6.4 | Final report | 12–15 pages instead of 20–30 |

## After v1.0 (v1.1)

Upgrade each lite task to full: a real site survey, earthing checks on every
circuit, a Class 4 CAPEX from supplier quotes, a second reviewer and the full
20–30 page report.
