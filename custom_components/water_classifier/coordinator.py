"""Coordinator for Water Pattern Classifier.

Classification cascade rules based on WEUSEDTO / REUWS / AutoFlow.
Order matters: from most specific (=long duration + volume) to most generic.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from .const import (
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


def classify_session(
    volume_l: float,
    duration_s: float,
    avg_flow_lmin: float,
    peak_flow_lmin: float | None = None,
    hour_of_day: int | None = None,
    thresholds: dict[str, Any] | None = None,
) -> str:
    """Classify a water session based on features.

    Args:
        volume_l: total volume in liters
        duration_s: session duration in seconds
        avg_flow_lmin: average flow rate in L/min
        peak_flow_lmin: peak flow rate in L/min (=optional, improves detection)
        hour_of_day: current hour 0-23 (=used for gardening detection)
        thresholds: dict of tunable thresholds (=see const.DEFAULTS)

    Returns:
        String classification from ALL_TYPES + TYPE_INCONNU.
    """
    if thresholds is None:
        from .const import DEFAULTS
        thresholds = DEFAULTS

    if volume_l <= 0:
        return TYPE_INCONNU

    t = thresholds
    peak = peak_flow_lmin or avg_flow_lmin

    # Cascade — from longest/most specific to shortest
    # 1. Long duration + high volume = machine à laver
    if duration_s > t["machine_duration_min_s"] and volume_l > 30:
        return TYPE_MACHINE

    # 2. Long duration + low volume = lave-vaisselle
    if duration_s > t["machine_duration_min_s"] and volume_l < 30:
        return TYPE_LAVE_VAISSELLE

    # 3. Very high volume + long duration = bain
    if (
        volume_l > t["bain_vol_min_l"]
        and duration_s > t["douche_duration_min_s"]
    ):
        return TYPE_BAIN

    # 4. Sustained HIGH flow (>8 L/min) during evening/morning hours = arrosage
    # NOTE: Must be checked BEFORE douche to distinguish (=douche typically <8 L/min)
    if (
        hour_of_day is not None
        and volume_l > t["arrosage_vol_min_l"]
        and duration_s > 300
        and avg_flow_lmin > 8
        and (
            hour_of_day >= t["arrosage_hour_start"]
            or hour_of_day < t["arrosage_hour_end"]
        )
    ):
        return TYPE_ARROSAGE

    # 5. Long sustained flow = douche (=débit modéré 4-8 L/min discrimine vs arrosage)
    if (
        duration_s > t["douche_duration_min_s"]
        and volume_l > t["douche_vol_min_l"]
        and avg_flow_lmin > 4
    ):
        return TYPE_DOUCHE

    # 6. WC : short-medium duration, medium volume, high peak
    if (
        t["wc_vol_min_l"] <= volume_l <= t["wc_vol_max_l"]
        and duration_s < t["wc_duration_max_s"]
        and peak > 4
    ):
        return TYPE_WC

    # 7. Very small volume + short duration = robinet/lavabo
    if (
        volume_l < t["robinet_vol_max_l"]
        and duration_s < t["robinet_duration_max_s"]
    ):
        return TYPE_ROBINET

    return TYPE_AUTRE


def get_current_hour() -> int:
    """Return current hour of day 0-23."""
    return datetime.now().hour
