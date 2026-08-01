"""Constants for the Water Pattern Classifier integration."""
from __future__ import annotations

DOMAIN = "water_classifier"

# Configuration keys
CONF_FLOW_SENSOR = "flow_sensor"
CONF_SESSION_VOLUME_SENSOR = "session_volume_sensor"
CONF_SESSION_DURATION_SENSOR = "session_duration_sensor"
CONF_SESSION_FLOW_SENSOR = "session_flow_sensor"

# Session types
TYPE_WC = "WC"
TYPE_DOUCHE = "Douche"
TYPE_BAIN = "Bain"
TYPE_MACHINE = "Machine à laver"
TYPE_LAVE_VAISSELLE = "Lave-vaisselle"
TYPE_ROBINET = "Robinet/Lavabo"
TYPE_ARROSAGE = "Arrosage"
TYPE_AUTRE = "Autre"
TYPE_INCONNU = "Inconnu"

ALL_TYPES = [
    TYPE_WC,
    TYPE_DOUCHE,
    TYPE_BAIN,
    TYPE_MACHINE,
    TYPE_LAVE_VAISSELLE,
    TYPE_ROBINET,
    TYPE_ARROSAGE,
    TYPE_AUTRE,
]

# Default thresholds (=based on WEUSEDTO / REUWS / AutoFlow)
DEFAULTS = {
    "wc_vol_min_l": 4.0,
    "wc_vol_max_l": 9.0,
    "wc_duration_max_s": 120,
    "douche_vol_min_l": 25.0,
    "douche_duration_min_s": 180,
    "bain_vol_min_l": 100.0,
    "machine_duration_min_s": 1800,
    "arrosage_vol_min_l": 50.0,
    "arrosage_hour_start": 18,
    "arrosage_hour_end": 8,
    "robinet_vol_max_l": 3.0,
    "robinet_duration_max_s": 60,
}
