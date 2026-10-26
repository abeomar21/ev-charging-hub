import pytest

from calcs import chargers


@pytest.fixture(scope="module")
def rows():
    return {r["id"]: r for r in chargers.load()}


def test_three_ac_and_three_dc(rows):
    roles = [r["role"] for r in rows.values()]
    assert roles.count("AC") == 3 and roles.count("DC") == 3


def test_every_row_has_a_source(rows):
    assert all(r["source_url"].startswith("https://") for r in rows.values())


def test_chosen_dc_uses_datasheet_current(rows):
    i, basis = chargers.design_current(rows["DC-1"])
    assert basis == "datasheet" and i == 94


def test_derived_current_is_below_datasheet(rows):
    # Sungrow IDC80E: 60 kW, 97 %, PF 0.99 at 400 V -> about 90 A, datasheet says 94 A
    d = chargers.derived_input_current(60, 0.97, 0.99)
    assert d == pytest.approx(90.2, abs=0.1)
    assert d < float(rows["DC-1"]["input_current_a"])


def test_missing_current_falls_back_to_derived(rows):
    i, basis = chargers.design_current(rows["DC-2"])
    assert basis == "derived" and i == pytest.approx(91.1, abs=0.2)
