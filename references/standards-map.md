# Standards and regulations map

**Task:** T0.4 · **Assumption link:** A03 (code basis) · **Status:** draft, clauses being verified

This file says which document governs which part of the EV hub design, and which clauses the
calcs and docs cite. It holds titles, editions and clause numbers only. No standard text is
copied here and no paid PDFs are committed (working rule 5).

## How to read the Status column

| Status | Meaning |
|---|---|
| `TO VERIFY` | Clause number taken from a secondary source (Schneider EIG, a textbook, a summary). Not yet checked against the standard itself. |
| `VERIFIED` | Checked against the named edition. Add who/where in the Notes column (e.g. "Ain Shams library, 2026-10-24"). |
| `SUPERSEDED` | A newer edition exists; the row says which one the project uses and why. |

A clause is only cited in `docs/` once its row is `VERIFIED`, or the citation carries the same flag.

---

## 1. Installation design: IEC 60364 series

| ID | Document | Edition used | Governs in this project | Clauses / tables cited | Tasks | Status |
|---|---|---|---|---|---|---|
| S01 | IEC 60364-7-722 · Low-voltage electrical installations, Part 7-722: Supplies for electric vehicles | 2018 | The EV-specific rules on top of the general parts: demand, earthing, RCDs, overcurrent per connecting point | 722.311 (maximum demand, no diversity without load control); 722.312.2.1 (earthing arrangement of EV final circuits); 722.531 (one RCD per connecting point, Type B or Type A + 6 mA DC detection); 722.533 (one overcurrent device per connecting point); 722.55 (socket-outlets and connectors) | T0.4, T2.2, T3.5, T3.6 | TO VERIFY |
| S02 | IEC 60364-5-52 · Selection and erection of electrical equipment: Wiring systems | 2009 + AMD1:2011 | Cable ampacity, derating and voltage drop | Table A.52.3 (installation methods); 523 + Annex B (current-carrying capacities, Tables B.52.2 to B.52.13); B.52.14 (air ambient ≠ 30 °C); B.52.15 (ground ≠ 20 °C); B.52.16 (soil thermal resistivity); B.52.17 to B.52.21 (grouping); 525 + Annex G, Table G.52.1 (voltage-drop limits) | T3.2, T3.3 | TO VERIFY |
| S03 | IEC 60364-4-43 · Protection for safety: Protection against overcurrent | 2008 | Coordination of cable and protective device; short-circuit withstand | 433.1 (Ib ≤ In ≤ Iz and I2 ≤ 1.45·Iz); 434.5.2 (adiabatic limit, k²S² ≥ I²t) | T3.2, T3.5, T3.7 | TO VERIFY |
| S04 | IEC 60364-4-41 · Protection for safety: Protection against electric shock | 2005 + AMD1:2017 | Automatic disconnection of supply in TN-S | 411.3.2 + Table 41.1 (maximum disconnection times); 411.4 (TN systems, Zs·Ia ≤ U0); 411.3.3 (additional protection by 30 mA RCD) | T3.6 | TO VERIFY |
| S05 | IEC 60364-5-54 · Earthing arrangements and protective conductors | 2011 | Earth electrode, PE and bonding conductor sizes | 542 (earthing arrangements, electrodes); 543.1 (PE cross-section, table method or adiabatic) | T3.6 | TO VERIFY |
| S06 | IEC 60364-5-53 · Devices for protection, isolation, switching, control and monitoring | 2019 + AMD1:2020 | RCD type selection, surge protective devices at the MDB | 531 (RCD selection and erection); 534 (SPD selection and erection) | T3.1, T3.5 | TO VERIFY |
| S07 | IEC 60364-4-44 · Protection against voltage and electromagnetic disturbances | 2007 + AMD2:2018 | Whether an SPD is required at the origin | 443 (protection against transient overvoltages) | T3.1 | TO VERIFY |
| S08 | IEC 60364-6 · Verification | 2016 | The commissioning checklist and its pass criteria | 6.4.2 (inspection); 6.4.3.2 (continuity); 6.4.3.3 + Table 6.1 (insulation resistance); 6.4.3.6 (polarity); 6.4.3.7 (automatic disconnection: loop impedance, earth resistance); 6.4.3.8 (additional protection, RCD tests); 6.4.3.9 (phase sequence); 6.4.3.10 (functional tests) | T6.1 | TO VERIFY |

## 2. EV charging equipment and protocol

| ID | Document | Edition used | Governs in this project | Clauses / tables cited | Tasks | Status |
|---|---|---|---|---|---|---|
| S10 | IEC 61851-1 · EV conductive charging system, Part 1: General requirements | 2017 | Charging modes, control pilot, states A to F, PWM duty cycle → current | Mode definitions (clause 6); Annex A (control pilot function, states table, duty-cycle-to-current table) | T0.3 | TO VERIFY |
| S11 | IEC 61851-23 · DC electric vehicle supply equipment | 2023 | What the 60 kW DC charger must comply with (cited from datasheets, not designed by us) | Cite only as "datasheet states compliance" | T1.3 | TO VERIFY |
| S12 | IEC 61851-24 · Digital communication between DC EVSE and EV | 2023 | Background only: the charger-to-car link, separate from OCPP | — | T0.3 | TO VERIFY |
| S13 | IEC 62196-1 / -2 / -3 · Plugs, socket-outlets, vehicle connectors and inlets | -2: 2022, -3: 2022 | Type 2 AC socket (62196-2, configuration type 2); CCS2 DC connector (62196-3, configuration FF) | Configuration names only | T0.3, T1.3 | TO VERIFY |
| S14 | IEC 61851-21-2 · EMC requirements for off-board EV charging systems | 2018 | Datasheet compliance check | — | T1.3 | TO VERIFY |
| S15 | OCPP 1.6 Edition 2 + OCPP-J 1.6 (Open Charge Alliance, free with registration) | 1.6 ed. 2, errata v4 | Simulator messages, connector status machine, smart charging | OCPP-J: RPC framework (CALL = 2, CALLRESULT = 3, CALLERROR = 4); OCPP 1.6: Core profile messages; Smart Charging profile (ChargePointMaxProfile, TxDefaultProfile, TxProfile, stack levels); SetChargingProfile | T4.2 to T4.8 | TO VERIFY |

## 3. Short circuit and power quality

| ID | Document | Edition used | Governs in this project | Clauses / tables cited | Tasks | Status |
|---|---|---|---|---|---|---|
| S20 | IEC 60909-0 · Short-circuit currents in three-phase AC systems: Calculation of currents | 2016 | Fault level at the MDB and each charger (by hand and via pandapower) | Equivalent voltage source method; Table 1 (voltage factor c); transformer impedance correction factor KT | T3.4 | TO VERIFY |
| S21 | IEC 61000-3-12 · Limits for harmonic currents, equipment with input current > 16 A and ≤ 75 A per phase | 2011 + AMD1:2021 | Harmonic check for the **22 kW AC chargers (32 A)** | Scope clause; harmonic limit tables vs Rsce | T2.6 | TO VERIFY |
| S22 | IEC TR 61000-3-4 · Limitation of harmonic current emissions, equipment with rated current > 75 A | 1998 | Harmonic check for the **60 kW DC chargers (≈ 92 A)**, which fall outside S21's scope | Stage 1 to 3 assessment approach | T2.6 | TO VERIFY |
| S23 | IEEE 519 · Harmonic control in electric power systems | 2022 | Optional cross-check of total site THD at the point of supply | Current distortion limits at the PCC | T2.6 | TO VERIFY |

> **Scope note for T2.6:** S21 only covers equipment up to 75 A per phase. A 60 kW DC charger drawing about 92 A is outside it, so the DC check is done against S22 (or S23 at site level). Writing this down is better than silently applying S21 to the DC units.

## 4. Product standards for equipment you select

Cited when a datasheet or catalogue claims compliance. Not designed against directly.

| ID | Document | Used for | Tasks |
|---|---|---|---|
| S30 | IEC 60898-1 | MCBs (B/C/D curves) on AC and aux circuits | T3.5 |
| S31 | IEC 60947-2 | MCCBs on DC charger feeders and the incomer; breaking capacity Icu/Ics | T3.4, T3.5 |
| S32 | IEC 61008-1 / IEC 61009-1 | RCCBs / RCBOs, Type AC and A | T3.5 |
| S33 | IEC 62423 | Type B and Type F RCDs | T3.5 |
| S34 | IEC 62955 | RDC-DD (6 mA DC detection) built into AC chargers | T3.5 |
| S35 | IEC 61643-11 | SPDs at the MDB | T3.1 |
| S36 | IEC 61439-1 / -2 | MDB and sub-boards as LV assemblies | T3.1, T5.1 |
| S37 | IEC 60076-1 | Distribution transformer rating and %Z | T2.5, T3.4 |
| S38 | IEC 60502-1 | XLPE/PVC LV power cables (Elsewedy catalogue basis) | T3.2 |
| S39 | IEC 60228 | Conductor classes and maximum DC resistance | T3.3 |
| S40 | IEC 60529 / IEC 62262 | IP and IK ratings of outdoor chargers | T1.3 |
| S41 | IEC 60617 / IEC 61082-1 | SLD graphical symbols and diagram conventions | T3.1 |

## 5. Egypt: law, regulator and tariffs

| ID | Document / source | What it sets for this project | Tasks | Status |
|---|---|---|---|---|
| E01 | Electricity Law No. 87 of 2015 and its executive regulations (PM Decree No. 230 of 2016) | EgyptERA's mandate to license activities and set tariffs | T0.4 | TO VERIFY |
| E02 | EgyptERA rules for EV charging station investment and licensing | Only licensed operators run public charging stations, under a contract with the distribution company; the operator is the "customer" of the DisCo | T0.4, T5.3 | TO VERIFY: locate the current text on egyptera.org |
| E03 | Ministerial Decision No. 101 of 2025 (EV charging tariff), Official Gazette | Station buys energy at the normal tariff for its **supply voltage level**; resale cap **1.45 ×** supply price for AC ≤ 22 kW, **2.8 ×** for DC | T5.3, T5.4 | VERIFIED via press reports of the Gazette text; confirm against the Gazette or EgyptERA page |
| E04 | EgyptERA Electric Power Connection Rules (2020) | How a new supply is requested; LV vs MV connection, which drives DEC-03 | T2.5 | TO VERIFY |
| E05 | EgyptERA current tariff schedule (commercial / by voltage level) | The supply price that E03's multipliers apply to. Prices changed in 2026, so record the date pulled. | T5.3 | Pull on the day of T5.3 |
| E06 | CCS2 requirement for public DC fast charging (from April 2025) | Connector choice for the DC units (A05) | T1.3 | Carried from plan; source: EV24 |
| E07 | EgyptERA EV rules summary: DC fast charging = above 22 kW per point; separate smart metering for EV stations | Charger classification and metering point on the SLD | T3.1 | Carried from plan; source: Riad & Riad summary |
| E08 | Egyptian code of practice for LV electrical installations in buildings | Check whether a national code applies alongside IEC 60364. If yes, record its number and edition; A03 keeps IEC 60364 as the design basis. | T0.4 | TO VERIFY |

## 6. Which standard to open for which question

| Question | Open |
|---|---|
| How many amps per phase, and is diversity allowed? | S01 722.311 + S02 |
| What cable size, with 40 °C air / 30 °C ground? | S02 Annex B + S03 433.1 |
| Is the voltage drop acceptable? | S02 Annex G, Table G.52.1 |
| What is the fault current at the MDB? | S20 + S37 (transformer %Z) |
| Will the cable survive the fault? | S03 434.5.2 |
| Which RCD for each charger? | S01 722.531 + S33 / S34 |
| Does the breaker disconnect in time? | S04 Table 41.1 + 411.4 |
| Do the chargers pass harmonics? | S21 (AC), S22 / S23 (DC) |
| How is the installation tested? | S08 |
| What can I charge the driver? | E03 + E05 |

## 7. Sources used to build this map

- Schneider Electric, *Electrical Installation Guide* (current edition), EV chapter and the cable / protection chapters, for the IEC 60364 clause references.
- EgyptERA website, Regulations section: "Electric Vehicle Charging Tariff" and "Electric Power Connection Rules 2020" pages.
- Egypt Independent, report on Ministerial Decision No. 101 of 2025 (EV charging tariff).
- EnterpriseAM, 7 Sep 2025, report on the AC 1.45× / DC 2.8× markups.
- Open Charge Alliance, OCPP 1.6 edition 2 download page.
- IEC Webstore catalogue pages for titles and current editions (free to browse, no text copied).
