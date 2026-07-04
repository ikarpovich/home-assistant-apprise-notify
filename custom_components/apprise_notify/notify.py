"""Notify platform for Apprise API."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    ATTR_TITLE,
    ATTR_TITLE_DEFAULT,
    BaseNotificationService,
)
from homeassistant.components.notify import (
    PLATFORM_SCHEMA as NOTIFY_PLATFORM_SCHEMA,
)
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .client import AppriseApiClient, AppriseApiError, build_payload

_LOGGER = logging.getLogger(__name__)

CONF_TIMEOUT = "timeout"
DEFAULT_TIMEOUT = 10

PLATFORM_SCHEMA = NOTIFY_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_URL): cv.url,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    }
)


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> AppriseApiNotificationService:
    """Get the Apprise API notification service."""
    return AppriseApiNotificationService(
        AppriseApiClient(config[CONF_URL], timeout=config[CONF_TIMEOUT])
    )


class AppriseApiNotificationService(BaseNotificationService):
    """Send Home Assistant notifications through an Apprise API endpoint."""

    def __init__(self, client: AppriseApiClient) -> None:
        """Initialize the notification service."""
        self._client = client

    def send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a message through Apprise API."""
        payload = build_payload(
            message=message,
            title=kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT),
            data=kwargs.get(ATTR_DATA),
            target=kwargs.get(ATTR_TARGET),
        )

        try:
            self._client.notify(payload)
        except AppriseApiError as err:
            _LOGGER.error("Failed to send Apprise notification: %s", err)
            raise HomeAssistantError(str(err)) from err
