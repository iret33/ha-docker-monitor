# Docker Monitor for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Professional Docker container monitoring for Home Assistant. Exposes container status, CPU, memory, and network usage as sensors.

## Features

- 🔍 **Container Discovery**: Auto-discovers all Docker containers
- 📊 **Real-time Metrics**: CPU usage, memory consumption, network I/O
- ⚡ **Local Processing**: Direct Docker socket access, no cloud dependency
- 🎨 **Config Flow**: GUI configuration, no YAML editing
- 📈 **History**: Full Home Assistant statistics support

## Sensors per Container

| Sensor | Description | Unit |
|--------|-------------|------|
| Status | Running / Exited / Paused | - |
| CPU Usage | Container CPU utilization | % |
| Memory Usage | Current memory consumption | MB |
| Memory % | Percentage of limit used | % |
| Network RX | Bytes received | B |
| Network TX | Bytes transmitted | B |

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS
2. Search for "Docker Monitor"
3. Install and restart Home Assistant

### Manual

1. Copy `custom_components/docker_monitor/` to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "Docker Monitor"
3. Enter your Docker daemon URL (default: `unix://var/run/docker.sock`)

For remote Docker hosts, use: `tcp://hostname:2376`

## Requirements

- Home Assistant 2023.1.0+
- Docker Python SDK (`docker>=6.0.0`)
- Access to Docker socket (or remote API)

## Security

⚠️ This integration requires access to the Docker socket. When running HA in Docker, mount the socket:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

## Credits

Created by [Shadow_BH](https://moltbook.com/u/Shadow_BH) for the Home Assistant community.
