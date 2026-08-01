"""Tests for the classification cascade — imports coordinator directly."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

# Load const.py and coordinator.py directly without triggering __init__.py
# (which imports homeassistant modules unavailable in a pure test env).
BASE = Path(__file__).parent.parent / "custom_components" / "water_classifier"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"_wc_{name}", BASE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"_wc_{name}"] = module
    spec.loader.exec_module(module)
    return module


_const = _load("const")

# coordinator uses `from .const import ...` — provide a shim so it can resolve
sys.modules["_wc_coordinator._const"] = _const


def _load_coordinator():
    """Load coordinator with patched relative-import base."""
    src = (BASE / "coordinator.py").read_text()
    # Replace relative imports with our loaded const module
    src = src.replace("from .const import", "from _wc_const import")
    sys.modules["_wc_const"] = _const
    exec_globals: dict = {}
    exec(compile(src, str(BASE / "coordinator.py"), "exec"), exec_globals)
    return exec_globals


_coord = _load_coordinator()
classify_session = _coord["classify_session"]

TYPE_WC = _const.TYPE_WC
TYPE_DOUCHE = _const.TYPE_DOUCHE
TYPE_BAIN = _const.TYPE_BAIN
TYPE_MACHINE = _const.TYPE_MACHINE
TYPE_LAVE_VAISSELLE = _const.TYPE_LAVE_VAISSELLE
TYPE_ROBINET = _const.TYPE_ROBINET
TYPE_ARROSAGE = _const.TYPE_ARROSAGE
TYPE_AUTRE = _const.TYPE_AUTRE
TYPE_INCONNU = _const.TYPE_INCONNU


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
