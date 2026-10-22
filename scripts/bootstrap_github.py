"""Create the repo's labels, phase milestones and the 40 task issues (T0.1).

Uses the GitHub CLI, so run `gh auth login` first. Safe to re-run: labels,
milestones and issues that already exist (matched by name, title or task ID)
are skipped, never duplicated or overwritten.

    python scripts/bootstrap_github.py --dry-run
    python scripts/bootstrap_github.py
"""

import argparse
import json
import subprocess
import sys
import time

DEFAULT_REPO = "abeomar21/ev-charging-hub"

DAY_DATES = {
    1: ("2026-10-22", "Thu 22 Oct"),
    2: ("2026-10-23", "Fri 23 Oct"),
    3: ("2026-10-24", "Sat 24 Oct"),
    4: ("2026-10-25", "Sun 25 Oct"),
    5: ("2026-10-26", "Mon 26 Oct"),
    6: ("2026-10-27", "Tue 27 Oct"),
}

# (code, title, description, due day)
PHASES = [
    ("P0", "Foundations", "Repo, CI, three-phase refresher, EV charging basics, standards map", 1),
    ("P1", "Requirements", "Charter, site, charger selection (DEC-02), demand assumptions and the register", 1),
    ("P2", "Load and load management", "Connected load, diversity, session simulator, managed demand, supply sizing, harmonics", 2),
    ("P3", "SLD, cables and protection", "Single-line diagram, cable sizing, voltage drop, fault levels, protection, earthing", 3),
    ("P4", "OCPP 1.6J simulator", "SteVe backend, four simulated charge points, fault injection, smart charging under the site cap", 5),
    ("P5", "Cost and feasibility", "Bill of quantities, CAPEX estimate, revenue model, feasibility metrics", 5),
    ("P6", "Commissioning, review and release", "Commissioning checklist, charger tests, external review, final report, v1.0", 6),
]

TYPES = [
    ("theory", "5319e7", "Learn the concept, write it down"),
    ("build", "1d76db", "Produce a calculation, drawing or code"),
    ("ship", "0e8a16", "Package, test, tag or release"),
]

LITE_LABEL = ("lite", "e58a00", "Ships in a lighter form; see ROADMAP.md")

PHASE_COLOURS = ["00a6cf", "00a6cf", "f29a00", "2b57ff", "0fa968", "f2306e", "7a4dff"]

# (id, title, day, type, description, lite note or None)
TASKS = [
    ("T0.1", "Repo, issues and Projects board", 1, "build",
     "Public ev-charging-hub repo with the folder skeleton. scripts/bootstrap_github.py creates the labels, "
     "7 milestones and 40 issues; Projects board with Todo / Doing / Done.", None),
    ("T0.2", "Three-phase power refresher", 1, "theory",
     "Line vs phase quantities, P = √3·U·I·cosφ, kW vs kVA, power factor. Output: 5 solved problems in "
     "docs/learning-log/, including the plan's 32.1 A and 92 A checks.", None),
    ("T0.3", "How EV charging works", 1, "theory",
     "AC (on-board charger) vs DC (off-board), Mode 3 vs Mode 4, Type 2 vs CCS2, control pilot states A–F and "
     "the PWM duty that sets current. Output: docs/00-background.md with one diagram.", None),
    ("T0.4", "Standards and regulations map", 1, "theory",
     "Which IEC part governs what: 60364-7-722, 60364-5-52, 60364-6, 61851-1, 62196, 60909, 61000-3-12; "
     "EgyptERA EV rules and tariff structure. Output: references/standards-map.md, titles and clauses only.", None),
    ("T0.5", "Python environment and CI", 1, "build",
     ".venv + requirements.txt, one passing pytest in GitHub Actions, CI badge in the README.", None),

    ("T1.1", "Project charter", 1, "build",
     "docs/01-charter.md with scope, exclusions and success criteria.", None),
    ("T1.2", "Site assessment", 1, "build",
     "A draw.io sketch of an assumed mall car park: bays, cable route, distance to the supply point in metres.",
     "Assumed site and a sketch with distances; no site visit"),
    ("T1.3", "Pick real chargers (DEC-02)", 1, "build",
     "Read 3 AC + 3 DC datasheets for input current, PF, THD, efficiency, IP/IK, standby power. Output: "
     "comparison table and DEC-02. Replace A08 with real PF and efficiency.", None),
    ("T1.4", "Demand assumptions A10–A20", 1, "build",
     "A10–A20: EV parc, session energy, dwell time, arrival pattern, each with a source or a TO VERIFY flag.", None),
    ("T1.5", "Assumptions register", 1, "build",
     "assumptions.csv is live: A01–A20, each with a value, unit, source and status (sourced or TO VERIFY).", None),

    ("T2.1", "Connected-load calculation", 2, "build",
     "Output power to input power through efficiency, kW to kVA to A per phase. calcs/load.py reads charger "
     "data from calcs/data/ and writes the table in docs/03-load.md. pytest asserts 22 kW ≈ 32 A and "
     "60 kW ≈ 92 A.", None),
    ("T2.2", "Diversity and demand factor", 2, "build",
     "One page with clause references: why IEC 60364-7-722 gives no diversity on unmanaged EV circuits, and "
     "when load management changes that.", None),
    ("T2.3", "Session simulator", 2, "build",
     "calcs/sessions.py: seeded random generator, Poisson arrivals with an hourly profile, session-energy and "
     "dwell distributions, 1,000 simulated days, per-minute site load written to CSV.", None),
    ("T2.4", "Unmanaged vs managed demand", 2, "build",
     "Unmanaged, static site cap and dynamic sharing. Load duration curves, peak kW for each, energy served vs "
     "energy delayed. The cap chosen here is what the simulator enforces in T4.6.", None),
    ("T2.5", "Size the supply (DEC-03)", 2, "build",
     "DEC-01: 2 × 60 kW vs 2 × 120 kW with both load studies. DEC-03: transformer kVA and utilisation, shared "
     "LV vs dedicated MV/LV kiosk.", None),
    ("T2.6", "Harmonics check", 2, "theory",
     "Datasheet THD against IEC 61000-3-12 limits, and why DC chargers dominate. One paragraph, pass or flag.",
     None),

    ("T3.1", "Single-line diagram, rev A", 3, "build",
     "Supply, transformer, MDB with metering point and SPD, 2 AC + 2 DC feeders and the aux board. IEC 60617 "
     "symbols, draw.io source and PDF in sld/.", None),
    ("T3.2", "Cable sizing by current", 3, "build",
     "calcs/data/cables.csv from the Elsewedy LV catalogue (ampacity, R and X per section, catalogue edition "
     "as source). calcs/cables.py sizes every circuit with Ib ≤ In ≤ Iz and derating for 40 °C air, 30 °C "
     "ground and grouping.", None),
    ("T3.3", "Voltage drop", 3, "build",
     "VD column in the cable schedule, ΔU = √3·I·L·(R cosφ + X sinφ) against the IEC 60364-5-52 Annex G "
     "limits, worst case highlighted. Sanity check: 92 A on 40 m of 50 mm² ≈ 0.8 %.", None),
    ("T3.4", "Short-circuit levels", 3, "build",
     "IEC 60909 method with pandapower: Ik at the MDB and at each charger from transformer %Z and source "
     "impedance; breaker breaking capacity checked in the schedule.", None),
    ("T3.5", "Protective devices (DEC-04)", 3, "theory",
     "MCB vs MCCB curves, selectivity, RCD Type A vs Type B and 6 mA DC detection. Output: protection schedule "
     "and DEC-04 RCD choice.", None),
    ("T3.6", "Earthing and bonding", 3, "build",
     "TN-S earthing note with a disconnection-time check.",
     "Earthing note and one disconnection-time check, not every circuit"),
    ("T3.7", "Cable short-circuit withstand", 3, "build",
     "Adiabatic k²S² ≥ I²t pass/fail column in the cable schedule.", None),

    ("T4.1", "Run SteVe locally", 4, "build",
     "docker compose up, UI reachable, CP01–CP04 and test idTags registered.", None),
    ("T4.2", "First connection", 4, "build",
     "With the ocpp package: BootNotification + Heartbeat accepted by SteVe over OCPP 1.6J.", None),
    ("T4.3", "Full transaction", 4, "build",
     "Authorize → StartTransaction → MeterValues → StopTransaction, visible in SteVe. Save the logs.", None),
    ("T4.4", "Model the hub", 4, "build",
     "Four charge points in one asyncio process; meter values driven by the T2.3 session model; replay a "
     "simulated day at accelerated time.", None),
    ("T4.5", "Fault injection, 5 scenarios", 4, "build",
     "Five scenarios with expected vs observed: connector fault, EV unplugged mid-session, backend offline with "
     "queued MeterValues, reconnect, rejected idTag.", None),
    ("T4.6", "Smart charging under the site cap", 4, "build",
     "SteVe pushes SetChargingProfile and the simulator honours it. Plot site kW against the cap for the "
     "replayed day.", None),
    ("T4.7", "Tests and CI", 4, "ship",
     "pytest-asyncio tests for the simulator, CI green. Tag v0.4.", None),
    ("T4.8", "Document the protocol", 5, "build",
     "docs/10-ocpp.md with Mermaid sequence diagrams for boot, a session, smart charging and one fault, plus "
     "captured logs.", None),

    ("T5.1", "Bill of quantities", 5, "build",
     "Take-off from the SLD and cable schedule into boq/boq.csv: item, spec, unit, qty, source.", None),
    ("T5.2", "CAPEX estimate", 5, "build",
     "Priced BoQ in EGP and USD; every price has a source and a date; estimate class and range stated.",
     "Class 5 from desk prices; Class 4 needs supplier quotes"),
    ("T5.3", "Revenue model", 5, "build",
     "calcs/economics.py: revenue under the EgyptERA EV tariff caps (AC up to 1.45× and DC 2.8× the supply "
     "price) at current supply prices.", None),
    ("T5.4", "Feasibility metrics and tornado", 5, "build",
     "NPV, IRR, simple payback and break-even utilisation, tornado chart, docs/08-economics.md.", None),

    ("T6.1", "Commissioning checklist", 5, "build",
     "docs/09-commissioning.md: IEC 60364-6 dead tests before live tests (continuity, insulation resistance, "
     "polarity, earth resistance, loop impedance, RCD trip tests, phase rotation, functional tests), each with "
     "pass criteria.", None),
    ("T6.2", "Charger-level tests", 5, "build",
     "Charger tests with pass criteria: CP/PP signalling, emergency stop, metering check, OCPP online.", None),
    ("T6.3", "External design review", 5, "build",
     "Log each reviewer comment as an issue, fix it, close it with a commit. No reply yet? Keep the issue open "
     "and write 'external review pending' in the README.",
     "One reviewer, weekend turnaround; marked pending if no reply"),
    ("T6.4", "Final report", 6, "build",
     "report/ PDF assembled from docs/: design basis, load study, electrical design, simulator, economics, "
     "commissioning, limitations. Every figure points to the script that made it.",
     "12–15 pages instead of 20–30"),
    ("T6.5", "Release v1.0 and summary", 6, "ship",
     "CHANGELOG, GitHub release with the report attached, one-page summary PDF. ROADMAP.md lists what v1.1 "
     "adds.", None),
]


def gh(*args, payload=None):
    """Run a gh command and return its parsed JSON output (None if empty)."""
    result = subprocess.run(
        ["gh", *args],
        input=json.dumps(payload).encode("utf-8") if payload is not None else None,
        capture_output=True,
    )
    if result.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
    out = result.stdout.decode("utf-8").strip()
    return json.loads(out) if out else None


def post(repo, endpoint, payload, dry_run):
    if dry_run:
        return {"number": 0}
    return gh("api", f"repos/{repo}/{endpoint}", "--method", "POST", "--input", "-", payload=payload)


def milestone_title(code, title):
    return f"{code} · {title}"


def ensure_labels(repo, dry_run):
    existing = {label["name"] for label in gh("label", "list", "-R", repo, "--limit", "200", "--json", "name")}
    wanted = [(f"phase: {code}", PHASE_COLOURS[i], title) for i, (code, title, _, _) in enumerate(PHASES)]
    wanted += [(f"type: {name}", colour, desc) for name, colour, desc in TYPES]
    wanted.append(LITE_LABEL)
    for name, colour, desc in wanted:
        if name in existing:
            print(f"label     skip    {name}")
            continue
        post(repo, "labels", {"name": name, "color": colour, "description": desc}, dry_run)
        print(f"label     create  {name}")


def ensure_milestones(repo, dry_run):
    """Return {phase code: milestone number}."""
    existing = {m["title"]: m["number"] for m in gh("api", f"repos/{repo}/milestones?state=all&per_page=100")}
    numbers = {}
    for code, title, desc, day in PHASES:
        full_title = milestone_title(code, title)
        if full_title in existing:
            numbers[code] = existing[full_title]
            print(f"milestone skip    {full_title}")
            continue
        # Noon UTC keeps the due date on the same calendar day in Cairo.
        due_on = f"{DAY_DATES[day][0]}T12:00:00Z"
        created = post(repo, "milestones", {"title": full_title, "description": desc, "due_on": due_on}, dry_run)
        numbers[code] = created["number"]
        print(f"milestone create  {full_title}")
    return numbers


def issue_body(task_id, day, description, lite):
    code = task_id[:2].replace("T", "P")
    phase_title = next(title for c, title, _, _ in PHASES if c == code)
    lines = [
        description,
        "",
        f"- **Phase:** {code} · {phase_title}",
        f"- **Day:** {day} ({DAY_DATES[day][1]})",
        f"- **Ships as:** {'Lite' if lite else 'Full'}",
    ]
    if lite:
        lines.append(f"- **Lite means:** {lite}")
    return "\n".join(lines)


def ensure_issues(repo, milestones, dry_run):
    issues = gh("issue", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", "title")
    existing_ids = {issue["title"].split()[0].rstrip(":") for issue in issues if issue["title"]}
    for task_id, title, day, kind, description, lite in TASKS:
        if task_id in existing_ids:
            print(f"issue     skip    {task_id}")
            continue
        code = task_id[:2].replace("T", "P")
        labels = [f"phase: {code}", f"type: {kind}"] + (["lite"] if lite else [])
        payload = {
            "title": f"{task_id}: {title}",
            "body": issue_body(task_id, day, description, lite),
            "milestone": milestones[code],
            "labels": labels,
        }
        created = post(repo, "issues", payload, dry_run)
        print(f"issue     create  {task_id} #{created['number']}")
        if not dry_run:
            time.sleep(1)  # stay clear of GitHub's secondary rate limit on content creation


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=DEFAULT_REPO, help=f"owner/name (default {DEFAULT_REPO})")
    parser.add_argument("--dry-run", action="store_true", help="print what would be created, change nothing")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    assert len(TASKS) == 40, f"expected 40 tasks, found {len(TASKS)}"
    ensure_labels(args.repo, args.dry_run)
    milestones = ensure_milestones(args.repo, args.dry_run)
    ensure_issues(args.repo, milestones, args.dry_run)


if __name__ == "__main__":
    main()
