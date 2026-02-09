"""Config flow for Docker Monitor."""
from __future__ import annotations

import logging
from typing import Any

import docker
from docker.errors import DockerException
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_HOST, default="unix://var/run/docker.sock"): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Docker Monitor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self._test_connection(user_input[CONF_HOST])
            except DockerException:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id("docker_monitor")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Docker Monitor", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _test_connection(self, docker_url: str) -> None:
        """Test Docker connection."""
        def test():
            client = docker.DockerClient(base_url=docker_url)
            client.ping()
            client.close()
        
        await self.hass.async_add_executor_job(test)
