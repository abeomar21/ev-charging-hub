# DEC-02 · Charger models

| | |
|---|---|
| Status | Accepted, 26 Oct 2026 |
| Author | Abdelrahman Hany |
| Task | T1.3 |
| Depends on | A04 (2 × 22 kW AC), A05 (2 × 60 kW DC, CCS2), A07 (40 °C design ambient) |
| Feeds | A08, T2.1 load, T2.6 harmonics, T3.2 cable sizing, DEC-04 RCD, T5.1 BoQ |
| Data | `calcs/data/chargers.csv` → `docs/04-charger-comparison.md` (generated) |

## Question

Which real AC and DC chargers does the hub use, so that every later calculation
runs on datasheet values instead of the placeholders in A08?

## What the choice has to satisfy

1. **Connector:** Type 2 for AC and CCS2 for DC. EgyptERA requires CCS2 at public fast chargers (see "Why Type 2 and CCS2" below).
2. **Rating:** 22 kW three-phase at 32 A (A04) and 60 kW DC per charger (A05).
3. **Cairo ambient:** must run at the 40 °C design ambient (A07), with margin for sun on the enclosure.
4. **Outdoor public duty:** IP54 minimum, IK10 against vandalism and car impact.
5. **OCPP 1.6J:** the simulator in P4 speaks 1.6J; the real chargers must too.
6. **Grid-side data published:** PF, THDi, efficiency and input current, because T2.1 and T2.6 need them.
7. **Local support:** a supplier with an Egyptian channel for spares and warranty.

## Options

Full values and sources are in the generated table. Summary against the criteria:

| | Sungrow AC22E-01 | ABB Terra AC W22 | Schneider EVlink Pro AC |
|---|---|---|---|
| Type 2, 22 kW, 32 A | ✓ tethered cable | ✓ socket | ✓ socket with shutter |
| IP / IK | **IP65** / IK10 | IP54 / IK10 | IP55 / IK10 |
| Max ambient | 50 °C | 50 °C | 50 °C |
| OCPP 1.6J | ✓ | ✓ | ✓ |
| Standby | **< 6.5 W** | not stated | not stated |
| Earth-fault protection | 6 mA DC detection inside; external RCD Type A or B needed | DC leakage detection inside | RCD Type B-EV inside (this reference) |
| Egyptian channel | **Electra, exclusive Sungrow agent** | ABB Egypt | Schneider Egypt |

| | Sungrow IDC80E (60 kW) | Autel MaxiCharger DC Fast 60 kW | Alpitronic HYC50 |
|---|---|---|---|
| CCS2, 60 kW | ✓ 1×60 or 2×30 | ✓ shared by 2 outlets | ✗ **50 kW only** |
| Input current | **94 A (datasheet)** | not stated (91 A derived) | 90 A (datasheet) |
| PF / THDi | ≥ 0.99 / < 5 % | ≥ 0.99 / ≤ 5 % | > 0.99 / < 5 % |
| Efficiency | 97 % max | 96 % peak | 97 % at full load |
| Standby | ≤ 50 W | not stated | 25 W |
| IP / IK | **IP65** / IK10 (HMI IK08) | IP55 / IK10 | not found |
| Max ambient | **60 °C, derates above 50 °C** | 55 °C, derates above 50 °C | 55 °C |
| OCPP | 1.6J (2.0.1 announced) | 1.6J (2.0.1 later) | 1.6 and 2.0.1 |
| Warranty | 3 years | 2 years | not found |

## Decision

**AC: Sungrow AC22E-01. DC: Sungrow IDC80E configured at 60 kW.**

Reasons, in order of weight:

1. **Most complete grid-side data.** The IDC80E is the only 60 kW candidate that
   publishes input current, PF, THDi, efficiency and standby on one sheet. That
   lets T2.1, T2.6 and T3.2 run on datasheet values with no "TO VERIFY" flags
   on the DC side.
2. **Best fit for Cairo heat.** IP65 on both units, and the IDC80E is rated to
   60 °C with derating above 50 °C. At 40 °C design ambient plus solar gain on
   the cabinet, it has the largest margin of the three DC options.
3. **Supply chain.** Electra (Raya Smart Buildings) holds the exclusive Sungrow
   agency in Egypt, so spares, warranty and firmware come through a local
   channel. In a real CPO, one hardware family also means one CSMS integration
   and one spares stock.
4. **OCPP 1.6J** on both, which matches the P4 simulator.

Why not the others:

- **ABB / Schneider AC:** both are good and IP54/IP55 is enough for a canopy.
  The Schneider B-EV reference would remove the external RCD (see DEC-04). They
  lost on ingress rating, published standby and supply channel, not on safety.
- **Autel DC:** the datasheet does not give input current or standby, so the
  design would rest on a derived number. Two-year warranty against three.
- **Alpitronic HYC50:** the best efficiency and standby figures, but it is 50 kW
  and would mean changing A05. It stays in the table as the benchmark.

## Consequences

- **A08 replaced** (rows in `assumptions_A08_patch.csv`):
  DC PF 0.99, THDi < 5 %, efficiency 0.97 (maximum), input current 94 A at 60 kW.
  AC wallbox efficiency 1.00 and standby 6.5 W; AC PF stays 0.99 but is now
  flagged as vehicle-dependent.
- **T2.1:** the 60 kW DC test value moves from the plan's 92 A to the datasheet
  94 A. The derived value at 400 V is 90.2 A; the datasheet figure is higher
  because it covers low grid voltage (the unit accepts 323–440 V) and losses
  below peak efficiency. Size cables on 94 A.
- **T2.6:** the DC chargers pass the harmonic screen at the charger terminals
  (THDi < 5 % at full power). IEC 61000-3-12 compliance is not stated on either
  sheet, so the harmonics note records it as a question for the supplier.
- **DEC-04:** the AC22E-01 detects 6 mA DC fault current internally and the
  datasheet asks for an external RCD Type A or B plus MCB per IEC 62955. That
  makes **Type A** sufficient on the AC circuits; Type B is not required.
- **Standby load:** 2 × 6.5 W + 2 × 50 W = 113 W continuous, about 990 kWh a
  year. Add it to the auxiliary load (A06).
- **The IDC80E has two CCS2 outlets** sharing 60 kW. Two units give four DC
  outlets at up to 60 kW each unit. The connected load is unchanged at
  2 × 60 kW; the extra outlet only matters for the session model in T2.3.
- **DEC-01 alternative noted:** Sungrow's IDC180E at its 120 kW setting gives
  60 kW × 2 from one cabinet (193 A input). It is the shared-cabinet route if
  DEC-01 moves towards a single power unit.

## Risks and open items

| Item | Status |
|---|---|
| IDC80E datasheet is Version 2 and marked "available in June" 2026 | Product is new; confirm availability in Egypt with Electra |
| 97 % is maximum efficiency, not at every load | Ask Sungrow for the efficiency curve; T2.3 energy model uses 0.97 until then |
| AC22E-01 is marketed for home use (tethered 5 m cable) | Acceptable under a canopy; the 7 m cable option suits angled bays |
| No Egyptian type approval listed on either sheet (SASO, ADQCC listed) | TO VERIFY with EgyptERA rules |
| ABB and Schneider standby not found | Not needed once Sungrow chosen; left blank, not zero |

## Why Type 2 and CCS2

- **EgyptERA mandate.** EgyptERA cancelled support for the Chinese GB/T protocol
  at public fast chargers and requires CCS2 exclusively. A GB/T car needs an
  adapter at a CCS2 charger.
- **CCS2 contains Type 2.** CCS2 ("Combo 2") is the Type 2 inlet with two DC pins
  added below it. A car with a CCS2 inlet takes a Type 2 plug for AC and the full
  CCS2 plug for DC, so choosing CCS2 for DC fixes Type 2 for AC.
- **Three-phase grid.** Type 2 carries three phases, which suits Egypt's
  400/230 V supply (A02) and is how 22 kW reaches the car at 32 A. Type 1 is a
  single-phase North American and Japanese connector.
- **Supplier range.** The Sungrow sheets read here offer CCS2 for DC and Type 2
  for AC only.

## Sources

Datasheet links are listed per charger in `docs/04-charger-comparison.md`. Others:

- EgyptERA CCS2 requirement: Enterprise (Arabic), "تحركات لحل أزمة شواحن السيارات الكهرب", <https://enterpriseam.com/egypt-ar/goinggreens/تحركات-لحل-أزمة-شواحن-السيارات-الكهرب/>
- Sungrow IDC180E 120 kW configuration: IDC180E datasheet V3, <https://evnow.conceptmaniax.gr/wp-content/uploads/2025/10/Sungrow-DC-180KW_IDC180E_Φύλλο_τεχνικών_δεδομένων.pdf>
- Electra–Sungrow exclusive agency: Electra company profile (project file, 24 Oct 2026) and Raya Holding release, <https://rayacorp.com/180kw-benchmark-raya-smart-buildings-and-sungrow-double-down-on-electra-as-egypts-fastest-ev-charging-network/>
