# 02b — Demand assumptions (T1.4)

**Site:** Mobil fuel station, Hadayek October (Giza), at the junction of Ahmed Zewail Road and the 6th of October–Wadi El Natrun road (S1 in `docs/02-site.md`).
**What this file answers:** how many cars will come, how much electricity each one takes, how long it stays, and what time it arrives.
**Where the numbers live:** rows A10–A20 in `assumptions.csv` (readable table in `docs/assumptions-register.md`). Rows marked DERIVED are calculated by `calcs/demand_check.py`, not typed by hand.

## The answer in one table (year 1, base case)

| Question | Fast charger (60 kW DC) | Slow charger (22 kW AC) | Row |
|---|---|---|---|
| Cars per charger per day | 4 (range 2–7) | 1.5 (range 0.5–3) | A12, A13 |
| Electricity per car | 34 kWh | 10 kWh | A15, A16 |
| Time plugged in | 41 min | 60 min | A17, A18 |
| Busiest time | 18:00–20:00 | 18:00–20:00 | A14 |
| Growth per year | 24 % | 24 % | A20 |

About 20,000 EVs are on the road in Greater Cairo today (A10).

## Why a fuel station changes the numbers

People stop at a fuel station for minutes, not hours.

- **Fast charging is the main product.** A 40-minute stop fits a coffee break.
- **Slow charging needs a reason.** A 22 kW point only makes sense if someone stays about an hour: ride-hailing drivers on a break, café customers, station staff or nearby residents.
- **Arrivals follow the road.** Few cars at night, busiest in the evening rush.

## Which cars arrive (A11)

I took the July 2026 licensing figures for the top 10 EV brands in Egypt (1,024 cars), grouped them by size and picked one real car per group:

| Group | Example car | Brands counted | Share | Battery | DC energy per visit |
|---|---|---|---|---|---|
| Small electric | BYD Dolphin Surf | BYD (half), DFSK | 14 % | 43.2 kWh | 25.9 kWh |
| Mid electric | Geely EX5 | Geely, Nissan, BYD (half), Forthing, MG | 50 % | 60.2 kWh | 36.1 kWh |
| Large electric | Deepal S07 | Deepal (half), Zeekr, Xpeng | 18 % | 78 kWh | 46.8 kWh |
| Large range-extender | Rox 01 | Rox | 12 % | 56 kWh | 28.0 kWh |
| Mid range-extender | Deepal S07 REEV | Deepal (half) | 6 % | 31.7 kWh | 15.8 kWh |

Range-extenders have a battery plus a small petrol engine that only charges the battery. Egypt's ones have big batteries (the Rox 01 has 56 kWh), so they use fast chargers too.

## How the 34 kWh is calculated (A15)

1. **Each car fills part of its battery.** Electric cars arrive at about 20 % and leave at 80 %, because charging slows down a lot above 80 %. That is 60 % of the battery. Range-extenders charge 30 % → 80 %, so 50 %.
   - Example: Geely EX5 → 60.2 kWh × 0.6 = 36.1 kWh.
2. **Average the groups by how common they are.**
   0.14 × 25.9 + 0.50 × 36.1 + 0.18 × 46.8 + 0.12 × 28.0 + 0.06 × 15.8 = **34.4 kWh**
3. **Check against real data.** Tesla's network averages about 33–35 kWh per visit. 34 kWh is believable.

**Time plugged in (A17)** = energy ÷ charging power + 5 minutes to plug in and pay. For the Geely: 36.1 ÷ 60 × 60 + 5 = 41 minutes.

**Slow charger (A16)** = power the car can take × time it stays. Most cars only take 11 kW from a slow charger, range-extenders 6.6–7 kW, so the average is 10.3 kW × 1 hour ≈ 10 kWh.

## Two findings that matter later

1. **Slow chargers use about half their rating.** A 22 kW point charging an 11 kW car draws about 16 A per phase, not 32 A. Use the real draw for the load study (T2.3–T2.4). Keep 32 A for cable and breaker sizing (T3.2–T3.5), because the next car might take the full 22 kW.
2. **Fast chargers run at full power.** Every fully electric car in the mix can take at least 60 kW, so each DC charger draws its full 60 kW for most of a visit. Two cars on the DC chargers at once sets the site's peak, which is why load management matters in T2.4.

## How sure is each number?

| Row | Confidence | Why | How to make it stronger |
|---|---|---|---|
| A11 car specs, A19 | High | Manufacturer and EV-database spec sheets; two values are still TO VERIFY | Confirm the Rox 01 DC average and the Deepal S07 REEV AC rate |
| A11 shares | Medium | Real licensing data, but grouping brands is my judgement | Get licensing by model, not just brand |
| A15, A16, A17 | Medium | Calculated from A11, matches real-world data | Follows A11 |
| A10 | Medium | National total is solid; the Cairo share is a judgement | EV licensing by governorate |
| A20 | Medium | Published forecast | — |
| A12, A13, A14, A18 | Low (TO VERIFY) | No Egyptian charging-station data is public | Count cars entering the station for one busy and one quiet hour; ask a charging operator |

## Sources

- Licensed EVs Jul 2021–Jun 2024 (Insurance Pool via Xinhua): https://www.chinaservicesinfo.com/s/202407/31/WS66a9a3ca498ed2d7b7eb4f99/feature-popularity-of-chinese-made-evs-grow-rapidly-in-egypt.html
- 2025 EV sales (IDSC): https://www.youm7.com/story/2026/5/25/معلومات-الوزراء-مصر-تتصدر-دول-أفريقيا-من-حيث-عدد-السيارات/7428112
- July 2026 EV licensing, top 10 brands: https://www.masrawy.com/autos/autos_news/details/2026/8/6/3028932 and https://www.egypttelegraph.com/article/267615/
- February and March 2026 EV licensing: https://www.egypttelegraph.com/article/225492/ and https://www.egypttelegraph.com/article/233457/
- Licensed vehicles by governorate (CAPMAS 2023): https://en.amwalalghad.com/?p=157402
- EV sales growth forecast (Fitch Solutions): https://www.masrawy.com/autos/autos_news/details/2026/6/10/3000521/
- US fast-charger sessions per day (Paren 2025): https://evchargingstations.com/chargingnews/parens-2025-state-of-the-us-dc-fast-charging-industry-report/
- Energy per visit, Thailand: https://ph05.tci-thaijo.org/index.php/itechtru/article/view/302
- Energy per visit, Tesla network: https://evchargingstations.com/chargingnews/us-supercharger-usage-hits-new-records-during-thanksgiving-2025/
- Time-of-day pattern (INL EV Project): https://avt.inl.gov/sites/default/files/pdf/EVProj/126447-30174.dcfc-initexp.pdf
- Session length survey: https://findingspress.org/article/162484-exploring-electric-vehicle-driver-activities-and-expenditure-while-using-dc-fast-chargers/attachment/345937.pdf
- Car specs: BYD Dolphin Surf https://ev-database.org/car/3194/BYD-DOLPHIN-SURF-432-kWh-Boost · Geely EX5 https://resource.digitaldealer.com.au/pdf/170215834367b2cde233d6d543706180.pdf · Deepal S07 BEV https://www.changaneurope.com/dk/modeller/changan-deepal-s07/specifikationer · Deepal S07 REEV https://data.carnewschina.com/database/deepal/deepal-s07/2023/params · Rox 01 https://www.drivearabia.com/news/2025/03/19/first-look-rox-01-reev/
- Deepal S07 BEV and REEV sold in Egypt: https://almalnews.com/2104300/
