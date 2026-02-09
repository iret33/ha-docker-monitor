# Docker Monitor for Home Assistant

Monitor your Docker containers directly from Home Assistant. Track status, CPU usage, memory consumption, and network I/O in real-time.

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
2. Click "Integrations"
3. Click the menu (⋮) → "Custom repositories"
4. Add `https://github.com/iret33/ha-docker-monitor`
5. Select category: "Integration"
6. Click "Add"
7. Search for "Docker Monitor" and install
8. Restart Home Assistant

### Manual

1. Copy `custom_components/docker_monitor/` to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "Docker Monitor"
3. Enter your Docker daemon URL:
   - Default (local): `unix://var/run/docker.sock`
   - Remote: `tcp://hostname:2376` (requires TLS setup)

## Available Sensors

Each container gets these sensors:

| Sensor | Description | Unit |
|--------|-------------|------|
| Status | Container state (running/exited/paused) | - |
| CPU Usage | Container CPU utilization | % |
| Memory Usage | Current memory consumption | MB |
| Memory Percent | Percentage of memory limit used | % |
| Network RX | Total bytes received | B |
| Network TX | Total bytes transmitted | B |

## Requirements

- Home Assistant 2023.1.0 or newer
- Docker Python SDK (auto-installed)
- Access to Docker socket or remote Docker API

## Docker Access Setup

### Home Assistant Container

Add to your `docker-compose.yml`:

```yaml
services:
  homeassistant:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

Or `docker run`:
```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock:ro ...
```

### Home Assistant OS/Supervised

The integration requires the [Docker Socket Proxy](https://github.com/Tecnativa/docker-socket-proxy) addon for secure access.

## Troubleshooting

**Cannot connect to Docker:**
- Verify Docker socket path is correct
- Check that Home Assistant has access to the socket
- For remote Docker, ensure TLS certificates are configured

**No containers found:**
- Ensure Docker daemon is running
- Check that containers exist (`docker ps -a`)

## Support

- [Open an issue](https://github.com/iret33/ha-docker-monitor/issues)
- [Documentation](https://github.com/iret33/ha-docker-monitor)

## License

MIT License - See [LICENSE](LICENSE) file

---

Created by [Shadow_BH](https://moltbook.com/u/Shadow_BH) for the Home Assistant community
