"""Smoke test: proves pytest and CI run. Real calculation tests start in T2.1."""

import math


def test_three_phase_current_formula():
    # 22 kW AC charger at 400 V, cos phi = 1: I = P / (sqrt(3) * U) ≈ 31.8 A
    current = 22_000 / (math.sqrt(3) * 400)
    assert math.isclose(current, 31.75, abs_tol=0.01)
