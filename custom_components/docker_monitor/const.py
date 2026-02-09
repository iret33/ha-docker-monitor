"""Constants for Docker Monitor."""
from datetime import timedelta

DOMAIN = "docker_monitor"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

SENSOR_TYPES = {
    "status": ["Status", None, "mdi:docker"],
    "cpu_percent": ["CPU Usage", "%", "mdi:cpu-64-bit"],
    "memory_usage": ["Memory Usage", "B", "mdi:memory"],
    "memory_percent": ["Memory %", "%", "mdi:memory"],
    "network_rx": ["Network RX", "B", "mdi:download-network"],
    "network_tx": ["Network TX", "B", "mdi:upload-network"],
    "uptime": ["Uptime", None, "mdi:clock"],
}
