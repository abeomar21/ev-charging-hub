"""Keep the assumptions register honest. Runs in CI with the other tests."""
import shutil

import pytest

import assumptions as reg
import demand_check


@pytest.fixture(scope="module")
def rows():
    return reg.load()


def test_register_follows_every_rule(rows):
    assert reg.validate(rows) == []


def test_ids_cover_a01_to_a20_without_gaps(rows):
    numbers = {int(aid[1:3]) for aid in rows}
    assert numbers == set(range(1, 21))


def test_every_number_parses_and_has_a_unit(rows):
    for r in rows.values():
        if r["kind"] == "number":
            float(r["value"])
            assert r["unit"], r["id"]


def test_derived_rows_match_the_script(rows):
    """Fails if someone edits fleet_mix.csv, A05b, A09 or A18 and forgets --write."""
    d = demand_check.derive()
    for aid in demand_check.OWNED:
        assert float(rows[aid]["value"]) == round(d[aid]), (
            f"{aid} is {rows[aid]['value']} in the register but the script gives {d[aid]:.1f}; "
            "run python calcs/demand_check.py --write")


def test_get_returns_typed_values():
    assert reg.get("A05b") == 60.0
    assert reg.get("A08c") == 94.0
    assert reg.get("A11").name == "fleet_mix.csv"
    assert "Mobil" in reg.get("A01")
    assert reg.bounds("A12") == (2.0, 4.0, 7.0)


def test_validator_catches_bad_rows(tmp_path, rows):
    """The checks themselves work: break a copy of the register and expect complaints."""
    broken = {k: dict(v) for k, v in rows.items()}
    broken["A12"]["verify"] = ""                    # TO VERIFY with no way to check it
    broken["A15"]["source"] = "worked it out"       # DERIVED with no script
    broken["A08c"]["value"] = "about 94"            # not a number
    del broken["A09"]                               # numbering gap
    problems = " ".join(reg.validate(broken))
    for expected in ("A12:", "A15:", "A08c:", "A09: missing"):
        assert expected in problems


def test_set_value_round_trips(tmp_path):
    copy = tmp_path / "assumptions.csv"
    shutil.copy(reg.REGISTER, copy)
    reg.set_value("A15", "35", path=copy)
    assert reg.get("A15", path=copy) == 35.0
    assert reg.load(copy).keys() == reg.load().keys()
