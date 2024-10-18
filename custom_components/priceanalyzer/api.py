"""Sample API Client."""

from __future__ import annotations
from homeassistant.core import HomeAssistant


import json

import socket
from typing import Any

import aiohttp
import async_timeout


class IntegrationBlueprintApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntegrationBlueprintApiClientCommunicationError(
    IntegrationBlueprintApiClientError,
):
    """Exception to indicate a communication error."""


class IntegrationBlueprintApiClientAuthenticationError(
    IntegrationBlueprintApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise IntegrationBlueprintApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class IntegrationBlueprintApiClient:
    """Sample API Client."""

    def __init__(
        self, entity_id: str, session: aiohttp.ClientSession, hass: HomeAssistant
    ) -> None:
        """Sample API Client."""
        self._entity_id = entity_id
        self._session = (session,)
        self._hass = hass

    async def async_get_data(self) -> Any:
        """Get data from the API."""

        # return self.get_dummy_sensor()

        nordpool_entity = self._hass.states.get(self._entity_id)
        if nordpool_entity:
            self._state = nordpool_entity
        else:
            self._state = False

        return self._state

        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    def get_dummy_sensor(self) -> Any:
        return {
            "state": 0.24,
            "state_class": "total",
            "average": 0.20145833333333332,
            "off_peak_1": 0.16025,
            "off_peak_2": 0.1795,
            "peak": 0.23625,
            "min": 0.067,
            "max": 0.296,
            "mean": 0.2045,
            "unit": "kWh",
            "currency": "NOK",
            "country": "Norway",
            "region": "NO3",
            "low_price": False,
            "price_percent_to_average": 1.211168562564633,
            "today": [
                0.162,
                0.136,
                0.078,
                0.067,
                0.149,
                0.157,
                0.249,
                0.284,
                0.294,
                0.296,
                0.287,
                0.209,
                0.203,
                0.203,
                0.206,
                0.207,
                0.244,
                0.239,
                0.237,
                0.21,
                0.198,
                0.192,
                0.177,
                0.151,
            ],
            "tomorrow": [
                0.175,
                0.168,
                0.167,
                0.15,
                0.15,
                0.164,
                0.175,
                0.195,
                0.198,
                0.199,
                0.201,
                0.199,
                0.181,
                0.17,
                0.168,
                0.163,
                0.163,
                0.167,
                0.162,
                0.165,
                0.166,
                0.165,
                0.17,
                0.15,
            ],
            "tomorrow_valid": True,
            "raw_today": [
                {
                    "start": "2024-10-16T00:00:00+02:00",
                    "end": "2024-10-16T01:00:00+02:00",
                    "value": 0.162,
                },
                {
                    "start": "2024-10-16T01:00:00+02:00",
                    "end": "2024-10-16T02:00:00+02:00",
                    "value": 0.136,
                },
                {
                    "start": "2024-10-16T02:00:00+02:00",
                    "end": "2024-10-16T03:00:00+02:00",
                    "value": 0.078,
                },
                {
                    "start": "2024-10-16T03:00:00+02:00",
                    "end": "2024-10-16T04:00:00+02:00",
                    "value": 0.067,
                },
                {
                    "start": "2024-10-16T04:00:00+02:00",
                    "end": "2024-10-16T05:00:00+02:00",
                    "value": 0.149,
                },
                {
                    "start": "2024-10-16T05:00:00+02:00",
                    "end": "2024-10-16T06:00:00+02:00",
                    "value": 0.157,
                },
                {
                    "start": "2024-10-16T06:00:00+02:00",
                    "end": "2024-10-16T07:00:00+02:00",
                    "value": 0.249,
                },
                {
                    "start": "2024-10-16T07:00:00+02:00",
                    "end": "2024-10-16T08:00:00+02:00",
                    "value": 0.284,
                },
                {
                    "start": "2024-10-16T08:00:00+02:00",
                    "end": "2024-10-16T09:00:00+02:00",
                    "value": 0.294,
                },
                {
                    "start": "2024-10-16T09:00:00+02:00",
                    "end": "2024-10-16T10:00:00+02:00",
                    "value": 0.296,
                },
                {
                    "start": "2024-10-16T10:00:00+02:00",
                    "end": "2024-10-16T11:00:00+02:00",
                    "value": 0.287,
                },
                {
                    "start": "2024-10-16T11:00:00+02:00",
                    "end": "2024-10-16T12:00:00+02:00",
                    "value": 0.209,
                },
                {
                    "start": "2024-10-16T12:00:00+02:00",
                    "end": "2024-10-16T13:00:00+02:00",
                    "value": 0.203,
                },
                {
                    "start": "2024-10-16T13:00:00+02:00",
                    "end": "2024-10-16T14:00:00+02:00",
                    "value": 0.203,
                },
                {
                    "start": "2024-10-16T14:00:00+02:00",
                    "end": "2024-10-16T15:00:00+02:00",
                    "value": 0.206,
                },
                {
                    "start": "2024-10-16T15:00:00+02:00",
                    "end": "2024-10-16T16:00:00+02:00",
                    "value": 0.207,
                },
                {
                    "start": "2024-10-16T16:00:00+02:00",
                    "end": "2024-10-16T17:00:00+02:00",
                    "value": 0.244,
                },
                {
                    "start": "2024-10-16T17:00:00+02:00",
                    "end": "2024-10-16T18:00:00+02:00",
                    "value": 0.239,
                },
                {
                    "start": "2024-10-16T18:00:00+02:00",
                    "end": "2024-10-16T19:00:00+02:00",
                    "value": 0.237,
                },
                {
                    "start": "2024-10-16T19:00:00+02:00",
                    "end": "2024-10-16T20:00:00+02:00",
                    "value": 0.21,
                },
                {
                    "start": "2024-10-16T20:00:00+02:00",
                    "end": "2024-10-16T21:00:00+02:00",
                    "value": 0.198,
                },
                {
                    "start": "2024-10-16T21:00:00+02:00",
                    "end": "2024-10-16T22:00:00+02:00",
                    "value": 0.192,
                },
                {
                    "start": "2024-10-16T22:00:00+02:00",
                    "end": "2024-10-16T23:00:00+02:00",
                    "value": 0.177,
                },
                {
                    "start": "2024-10-16T23:00:00+02:00",
                    "end": "2024-10-17T00:00:00+02:00",
                    "value": 0.151,
                },
            ],
            "raw_tomorrow": [
                {
                    "start": "2024-10-17T00:00:00+02:00",
                    "end": "2024-10-17T01:00:00+02:00",
                    "value": 0.175,
                },
                {
                    "start": "2024-10-17T01:00:00+02:00",
                    "end": "2024-10-17T02:00:00+02:00",
                    "value": 0.168,
                },
                {
                    "start": "2024-10-17T02:00:00+02:00",
                    "end": "2024-10-17T03:00:00+02:00",
                    "value": 0.167,
                },
                {
                    "start": "2024-10-17T03:00:00+02:00",
                    "end": "2024-10-17T04:00:00+02:00",
                    "value": 0.15,
                },
                {
                    "start": "2024-10-17T04:00:00+02:00",
                    "end": "2024-10-17T05:00:00+02:00",
                    "value": 0.15,
                },
                {
                    "start": "2024-10-17T05:00:00+02:00",
                    "end": "2024-10-17T06:00:00+02:00",
                    "value": 0.164,
                },
                {
                    "start": "2024-10-17T06:00:00+02:00",
                    "end": "2024-10-17T07:00:00+02:00",
                    "value": 0.175,
                },
                {
                    "start": "2024-10-17T07:00:00+02:00",
                    "end": "2024-10-17T08:00:00+02:00",
                    "value": 0.195,
                },
                {
                    "start": "2024-10-17T08:00:00+02:00",
                    "end": "2024-10-17T09:00:00+02:00",
                    "value": 0.198,
                },
                {
                    "start": "2024-10-17T09:00:00+02:00",
                    "end": "2024-10-17T10:00:00+02:00",
                    "value": 0.199,
                },
                {
                    "start": "2024-10-17T10:00:00+02:00",
                    "end": "2024-10-17T11:00:00+02:00",
                    "value": 0.201,
                },
                {
                    "start": "2024-10-17T11:00:00+02:00",
                    "end": "2024-10-17T12:00:00+02:00",
                    "value": 0.199,
                },
                {
                    "start": "2024-10-17T12:00:00+02:00",
                    "end": "2024-10-17T13:00:00+02:00",
                    "value": 0.181,
                },
                {
                    "start": "2024-10-17T13:00:00+02:00",
                    "end": "2024-10-17T14:00:00+02:00",
                    "value": 0.17,
                },
                {
                    "start": "2024-10-17T14:00:00+02:00",
                    "end": "2024-10-17T15:00:00+02:00",
                    "value": 0.168,
                },
                {
                    "start": "2024-10-17T15:00:00+02:00",
                    "end": "2024-10-17T16:00:00+02:00",
                    "value": 0.163,
                },
                {
                    "start": "2024-10-17T16:00:00+02:00",
                    "end": "2024-10-17T17:00:00+02:00",
                    "value": 0.163,
                },
                {
                    "start": "2024-10-17T17:00:00+02:00",
                    "end": "2024-10-17T18:00:00+02:00",
                    "value": 0.167,
                },
                {
                    "start": "2024-10-17T18:00:00+02:00",
                    "end": "2024-10-17T19:00:00+02:00",
                    "value": 0.162,
                },
                {
                    "start": "2024-10-17T19:00:00+02:00",
                    "end": "2024-10-17T20:00:00+02:00",
                    "value": 0.165,
                },
                {
                    "start": "2024-10-17T20:00:00+02:00",
                    "end": "2024-10-17T21:00:00+02:00",
                    "value": 0.166,
                },
                {
                    "start": "2024-10-17T21:00:00+02:00",
                    "end": "2024-10-17T22:00:00+02:00",
                    "value": 0.165,
                },
                {
                    "start": "2024-10-17T22:00:00+02:00",
                    "end": "2024-10-17T23:00:00+02:00",
                    "value": 0.17,
                },
                {
                    "start": "2024-10-17T23:00:00+02:00",
                    "end": "2024-10-18T00:00:00+02:00",
                    "value": 0.15,
                },
            ],
            "current_price": 0.244,
            "additional_costs_current_hour": 0.0,
            "price_in_cents": False,
            "unit_of_measurement": "NOK/kWh",
            "device_class": "monetary",
            "icon": "mdi:flash",
            "friendly_name": "nordpool",
        }

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise IntegrationBlueprintApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise IntegrationBlueprintApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise IntegrationBlueprintApiClientError(
                msg,
            ) from exception
