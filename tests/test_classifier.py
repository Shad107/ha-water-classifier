"""Tests for the classification cascade."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components"))

from water_classifier.coordinator import classify_session  # noqa: E402
from water_classifier.const import (  # noqa: E402
    TYPE_ARROSAGE,
    TYPE_AUTRE,
    TYPE_BAIN,
    TYPE_DOUCHE,
    TYPE_INCONNU,
    TYPE_LAVE_VAISSELLE,
    TYPE_MACHINE,
    TYPE_ROBINET,
    TYPE_WC,
)


def test_wc_6l():
    assert classify_session(6.0, 60, 6.0, peak_flow_lmin=7.0) == TYPE_WC


def test_wc_edge_low():
    assert classify_session(4.5, 55, 5.0, peak_flow_lmin=6.5) == TYPE_WC


def test_wc_edge_high():
    assert classify_session(8.5, 80, 6.0, peak_flow_lmin=7.5) == TYPE_WC


def test_douche():
    assert classify_session(60, 480, 7.5, peak_flow_lmin=9.0) == TYPE_DOUCHE


def test_bain():
    assert classify_session(150, 720, 12.5, peak_flow_lmin=14.0) == TYPE_BAIN


def test_machine():
    assert classify_session(60, 5400, 0.7, peak_flow_lmin=8.0) == TYPE_MACHINE


def test_lave_vaisselle():
    assert classify_session(12, 5400, 0.15, peak_flow_lmin=4.0) == TYPE_LAVE_VAISSELLE


def test_robinet():
    assert classify_session(1.0, 15, 4.0, peak_flow_lmin=5.0) == TYPE_ROBINET


def test_arrosage_evening():
    assert classify_session(100, 600, 10.0, peak_flow_lmin=12.0, hour_of_day=19) == TYPE_ARROSAGE


def test_arrosage_morning():
    assert classify_session(100, 600, 10.0, peak_flow_lmin=12.0, hour_of_day=6) == TYPE_ARROSAGE


def test_arrosage_afternoon_ignored():
    r = classify_session(100, 600, 10.0, peak_flow_lmin=12.0, hour_of_day=14)
    assert r != TYPE_ARROSAGE


def test_zero_volume():
    assert classify_session(0, 0, 0) == TYPE_INCONNU


def test_ambiguous_autre():
    assert classify_session(20, 120, 10, peak_flow_lmin=15) == TYPE_AUTRE
