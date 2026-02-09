"""Sensor platform for Docker Monitor."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfInformation, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DockerDataUpdateCoordinator
from .const import DOMAIN, SENSOR_TYPES


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Docker Monitor sensor based on a config entry."""
    coordinator: DockerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for container_name, data in coordinator.data.items():
        for sensor_type in SENSOR_TYPES:
            if sensor_type in data or sensor_type == "status":
                entities.append(
                    DockerSensor(coordinator, container_name, sensor_type)
                )
    
    async_add_entities(entities)


class DockerSensor(CoordinatorEntity[DockerDataUpdateCoordinator], SensorEntity):
    """Representation of a Docker sensor."""
    
    def __init__(
        self,
        coordinator: DockerDataUpdateCoordinator,
        container_name: str,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._container_name = container_name
        self._sensor_type = sensor_type
        self._attr_name = f"{container_name} {SENSOR_TYPES[sensor_type][0]}"
        self._attr_unique_id = f"{container_name}_{sensor_type}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._attr_icon = SENSOR_TYPES[sensor_type][2]
        
        if sensor_type in ["memory_usage", "network_rx", "network_tx"]:
            self._attr_device_class = SensorDeviceClass.DATA_SIZE
            self._attr_suggested_display_precision = 2
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        container_data = self.coordinator.data.get(self._container_name, {})
        value = container_data.get(self._sensor_type)
        
        if self._sensor_type == "memory_usage" and value:
            return round(value / (1024 * 1024), 2)  # Convert to MB
        
        return value
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success and self._container_name in self.coordinator.data
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        container_data = self.coordinator.data.get(self._container_name, {})
        if self._sensor_type == "status":
            return {
                "container_id": container_data.get("id"),
                "image": container_data.get("image"),
            }
        return {}
