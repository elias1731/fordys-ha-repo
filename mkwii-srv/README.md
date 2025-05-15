# | 2. Fordy's Custom Mario Kart Wii Server

Ein MKWii-Server als Home Assistant Add-on.

![AddonIcon](https://raw.githubusercontent.com/elias1731/fordys-ha-repo/refs/heads/main/mkwii-srv/icon.png)

## 🏎️ • Addon
- [**Wiimmfi**](https://wiimmfi.de/) — ist die Basis des lokalen-Servers.
- Ein **DNS-Server** wird für die Nutzung an realen Wii-Konsolen bereitgestellt!

## 🛠️ • Konfiguration & Ports 
1. Installiere das Add-on in Home Assistant.
2. Folgende Ports werden verwendet:
  - **DNS**-Port: `53/udp`
  - **HTTP** (kein WebUI): `80/tcp`
  - Game-Server: `9000/tcp`
