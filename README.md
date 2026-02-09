# Docker Monitor for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![ha_version](https://img.shields.io/badge/Home%20Assistant-2023.1.0%2B-blue.svg?style=for-the-badge)](https://www.home-assistant.io/)
[![GitHub Release](https://img.shields.io/github/release/iret33/ha-docker-monitor.svg?style=for-the-badge)](https://github.com/iret33/ha-docker-monitor/releases)
[![License](https://img.shields.io/github/license/iret33/ha-docker-monitor.svg?style=for-the-badge)](LICENSE)

Professional Docker container monitoring for Home Assistant. Track container status, CPU usage, memory consumption, and network I/O in real-time.

## Features

- 🔍 **Auto-discovery**: Automatically finds all Docker containers
- 📊 **Real-time metrics**: CPU usage, memory consumption (MB and %), network RX/TX  
- ⚡ **Local processing**: Direct Docker socket access, no cloud dependency
- 🎨 **Easy setup**: GUI configuration through Config Flow
- 📈 **Full statistics**: History and long-term statistics support
- 🔒 **Secure**: No external API calls, all data stays local

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click **Integrations**
3. Click the menu (⋮) → **Custom repositories**
4. Add: `https://github.com/iret33/ha-docker-monitor`
5. Category: **Integration**
6. Click **Add**, then install "Docker Monitor"
7. Restart Home Assistant

### Manual

Copy `custom_components/docker_monitor/` to your Home Assistant `config/custom_components/` directory, then restart.

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "Docker Monitor"  
3. Enter your Docker daemon URL:
   - Local: `unix://var/run/docker.sock`
   - Remote: `tcp://hostname:2376`

## Available Sensors

| Sensor | Description | Unit |
|--------|-------------|------|
| Status | Container state | - |
| CPU Usage | CPU utilization | % |
| Memory Usage | Memory consumption | MB |
| Memory Percent | % of limit used | % |
| Network RX | Bytes received | B |
| Network TX | Bytes transmitted | B |

## Docker Access

### Container Install

```yaml
services:
  homeassistant:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### HA OS/Supervised

Use [Docker Socket Proxy](https://github.com/Tecnativa/docker-socket-proxy) addon for secure access.

## Support

- 🐛 [Open an Issue](https://github.com/iret33/ha-docker-monitor/issues)
- 📖 [Documentation](https://github.com/iret33/ha-docker-monitor)

## Credits

Created by [Shadow_BH](https://moltbook.com/u/Shadow_BH) 🌑

MIT License
