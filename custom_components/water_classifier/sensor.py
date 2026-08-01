"""Sensor platform for Water Pattern Classifier."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_FLOW_SENSOR,
    CONF_SESSION_DURATION_SENSOR,
    CONF_SESSION_FLOW_SENSOR,
    CONF_SESSION_VOLUME_SENSOR,
    DEFAULTS,
    DOMAIN,
    TYPE_INCONNU,
)
from .coordinator import classify_session

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entity."""
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LastSessionTypeSensor(entry, data)], True)


def _safe_float(state: State | None) -> float:
    """Coerce a state to float, 0.0 on failure."""
    if state is None:
        return 0.0
    try:
        return float(state.state)
    except (ValueError, TypeError):
        return 0.0


class LastSessionTypeSensor(SensorEntity):
    """Sensor exposing the classification of the last water session."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:water-check"
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry, data: dict[str, Any]) -> None:
        """Init sensor."""
        self._entry = entry
        self._data = data
        self._attr_unique_id = f"{entry.entry_id}_last_session_type"
        self._attr_name = "Last session type"
        self._attr_native_value = TYPE_INCONNU
        self._attributes: dict[str, Any] = {}

    async def async_added_to_hass(self) -> None:
        """Register listener on Water-Monitor session sensor."""
        tracked = [
            self._data[CONF_SESSION_VOLUME_SENSOR],
            self._data[CONF_SESSION_DURATION_SENSOR],
            self._data[CONF_SESSION_FLOW_SENSOR],
        ]
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                tracked,
                self._async_state_change,
            )
        )
        self._update()

    @callback
    def _async_state_change(self, _event: Any) -> None:
        """Handle upstream sensor changes."""
        self._update()
        self.async_write_ha_state()

    def _update(self) -> None:
        """Recompute classification."""
        v = _safe_float(self.hass.states.get(self._data[CONF_SESSION_VOLUME_SENSOR]))
        d = _safe_float(self.hass.states.get(self._data[CONF_SESSION_DURATION_SENSOR]))
        f = _safe_float(self.hass.states.get(self._data[CONF_SESSION_FLOW_SENSOR]))

        peak_state = self.hass.states.get(self._data[CONF_FLOW_SENSOR])
        peak = _safe_float(peak_state) if peak_state else f

        classification = classify_session(
            volume_l=v,
            duration_s=d,
            avg_flow_lmin=f,
            peak_flow_lmin=peak,
            hour_of_day=datetime.now().hour,
            thresholds=DEFAULTS,
        )
        self._attr_native_value = classification
        self._attributes = {
            "volume_l": v,
            "duration_s": d,
            "avg_flow_lmin": f,
            "peak_flow_lmin": peak,
        }

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return self._attributes
