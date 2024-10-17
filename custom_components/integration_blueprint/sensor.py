"""Sensor platform for priceanalyzer."""

from __future__ import annotations

import logging
import math
from datetime import datetime
from operator import itemgetter
from re import L
from statistics import mean
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)  # Import sensor entity and classes.

from .const import DOMAIN, LOGGER
from .entity import IntegrationBlueprintEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import IntegrationBlueprintConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="priceanalyzer",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationBlueprintConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        PriceAnalyzerSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class PriceAnalyzerSensor(IntegrationBlueprintEntity, SensorEntity):
    """priceanalyzer Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

        self.nordpool = self.coordinator.data

    @property
    def current_hour(self) -> list:
        if self.today is not None:
            now = datetime.now()
            return self.today[now.hour]
        return []

    @property
    def nordpool_today(self) -> list:
        return self.nordpool_attributes["raw_today"]

    @property
    def nordpool_tomorrow(self) -> list:
        return self.nordpool_attributes["raw_tomorrow"]

    @property
    def today(self) -> list:
        day = self.nordpool_today
        return self.calculate_day(day)

    @property
    def tomorrow(self) -> list:
        day = self.nordpool_tomorrow
        return self.calculate_day(day)

    @property
    def nordpool_attributes(self) -> dict:
        if self.nordpool.get("attributes") is not None:
            return self.nordpool.get("attributes")
        else:
            return self.nordpool

    @property
    def extra_state_attributes(self) -> dict:
        attributes = {
            "current_hour": self.current_hour,
            "raw_today": self.today,
            "raw_tomorrow": self.tomorrow,
        }
        return attributes

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""

        if self.current_hour:
            return str(self.current_hour.get("temp") or 0)  # type: ignore
        else:
            return str(0)

        nordpool_state = self.nordpool.state or ""
        return nordpool_state

    def calculate_correction_for_hour(self, time, get_reason=False) -> Any | None:
        hour = self.get_hour(time)

        # TODO: Implement the temperature logic from the orginal repo.

        if hour.get("value") < self.get_hour(time + 1).get("value"):  # type: ignore
            return 1 if get_reason is False else "Billig strøm"
        elif hour.get("value") > self.get_hour(time + 1).get("value"):  # type: ignore
            return -1 if get_reason is False else "Dyr strøm"
        return 0 if get_reason is False else "Vanlig strøm"

    def calculate_day(self, raw) -> list:
        calculated = []
        time = 0
        for hour in raw:
            # Convert string date to datetime object
            start_time = datetime.fromisoformat(hour["start"])

            # Get today's date
            today = datetime.now().date()

            # Check if the start date is today or tomorrow
            is_tomorrow = start_time.date() != today

            item = {
                "start": hour.get("start"),
                "end": hour.get("end"),
                "temp": self.calculate_correction_for_hour(time),
                "reason": self.calculate_correction_for_hour(time, True),
                "value": hour.get("value"),
                "price_next_hour": self.get_hour(time + 1).get("value"),  # type: ignore
                "is_tomorrow": is_tomorrow,
            }

            calculated.append(item)
            time += 1

        return calculated

    def get_hour(self, hour):
        if 0 <= hour < len(self.nordpool_today):
            value = self.nordpool_today[hour]
        else:
            # Calculate the fallback index within nordpool_tomorrow
            fallback_index = hour - len(self.nordpool_today)
            # Check if fallback index is valid for nordpool_tomorrow
            if 0 <= fallback_index < len(self.nordpool_tomorrow):
                value = self.nordpool_tomorrow[fallback_index]
            else:
                value = None  # Or any other default behavior you want

        return value

        is_tomorrow = False
        if is_tomorrow == False and (hour < len(self._someday(self._data_today))):
            return self._someday(self._data_today)[hour]
        elif (
            is_tomorrow == False
            and self.tomorrow_valid
            and (hour - 24 < len(self._someday(self._data_tomorrow)))
        ):
            return self._someday(self._data_tomorrow)[hour - 24]
        elif is_tomorrow and (hour < len(self._someday(self._data_tomorrow))):
            return self._someday(self._data_tomorrow)[hour]
        else:
            return None
