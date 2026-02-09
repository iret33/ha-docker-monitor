"""Docker Monitor integration for Home Assistant.

Monitors Docker containers and exposes their status, CPU, memory, and network usage as sensors.
"""
from __future__ import annotations

import logging
from typing import Any

import docker
from docker.errors import DockerException

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Docker Monitor from a config entry."""
    coordinator = DockerDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class DockerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from Docker."""
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self._docker_url = entry.data.get("docker_url", "unix://var/run/docker.sock")
        self._client: docker.DockerClient | None = None
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
    
    def _get_client(self) -> docker.DockerClient:
        """Get or create Docker client."""
        if self._client is None:
            self._client = docker.DockerClient(base_url=self._docker_url)
        return self._client
    
    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            return await self.hass.async_add_executor_job(self._update_data)
        except DockerException as err:
            _LOGGER.error("Docker connection error: %s", err)
            raise UpdateFailed(f"Docker error: {err}") from err
    
    def _update_data(self) -> dict[str, Any]:
        """Fetch data from Docker."""
        client = self._get_client()
        containers_data = {}
        
        for container in client.containers.list(all=True):
            stats = self._get_container_stats(container)
            containers_data[container.name] = {
                "id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "cpu_percent": stats.get("cpu_percent", 0),
                "memory_usage": stats.get("memory_usage", 0),
                "memory_limit": stats.get("memory_limit", 1),
                "memory_percent": stats.get("memory_percent", 0),
                "network_rx": stats.get("network_rx", 0),
                "network_tx": stats.get("network_tx", 0),
                "uptime": stats.get("uptime", 0),
            }
        
        return containers_data
    
    def _get_container_stats(self, container) -> dict[str, Any]:
        """Get statistics for a container."""
        try:
            if container.status != "running":
                return {}
            
            stats = container.stats(stream=False)
            
            # Calculate CPU percentage
            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )
            system_delta = (
                stats["cpu_stats"]["system_cpu_usage"]
                - stats["precpu_stats"]["system_cpu_usage"]
            )
            
            cpu_percent = 0.0
            if system_delta > 0 and cpu_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * len(
                    stats["cpu_stats"]["cpu_usage"]["percpu_usage"] or [1]
                ) * 100
            
            # Memory stats
            memory_usage = stats["memory_stats"].get("usage", 0)
            memory_limit = stats["memory_stats"].get("limit", 1)
            memory_percent = (memory_usage / memory_limit) * 100 if memory_limit > 0 else 0
            
            # Network stats
            networks = stats.get("networks", {})
            network_rx = sum(n.get("rx_bytes", 0) for n in networks.values())
            network_tx = sum(n.get("tx_bytes", 0) for n in networks.values())
            
            return {
                "cpu_percent": round(cpu_percent, 2),
                "memory_usage": memory_usage,
                "memory_limit": memory_limit,
                "memory_percent": round(memory_percent, 2),
                "network_rx": network_rx,
                "network_tx": network_tx,
            }
        except Exception as err:
            _LOGGER.debug("Error getting stats for %s: %s", container.name, err)
            return {}
