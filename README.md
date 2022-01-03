# VPNWatch

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/github/license/Lanjelin/Docker-VPNWatcher)

Notifies through Pushover should your Docker VPN-Client lose its connection, or expose your real IP.

Made and tested for [Gluetun VPN client](https://github.com/qdm12/gluetun)

To pull and run with docker compose.
```
version: "2.1"

  watcher:
    image: lanjelin/vpnwatch-watcher:latest
    network_mode: "container:gluetun"
    container_name: vpnwatch-watcher
    environment:
      # Required vars, see https://pushover.net/api for Pushover related
      - USER=<USER-KEY-GOES-HERE>
      - TOKEN=<API-TOKEN-GOES-HERE>
      - PUSHOVER=http://<IP:PORT-OF-NOTIFIER>/push
      - IP=<YOUR-WAN-IP-GOES-HERE>
      #Optional
      - TIMER=360  #how often to run, in seconds. defaults to 360s/5m
      - TITLE=VPNWatcher
      - PRIORITY=1
      - EXPIRE=120
      - RETRY=30
      - SOUND=tugboat
      - TZ=Europe/Oslo
    
  notifier:
    image: lanjelin/vpnwatch-notifier:latest
    container_name: vpnwatch-notifier
    environment:
      - TZ=Europe/Oslo
    ports:
      - 5000:5000
```
Gluetun needs the following environment variable to allow the connected containers to communicate with the local network.
```
  FIREWALL_OUTBOUND_SUBNETS: '192.168.1.0/24'
```
