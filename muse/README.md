# Muse Discord Music Bot Add-on

Dieses Add-on hostet den Muse Discord Music Bot basierend auf der offiziellen Docker-Compose-Konfiguration.

## Voraussetzungen
- **Discord-Bot-Token**: Über das [Discord Developer Portal](https://discord.com/developers/applications) erstellen.
- **YouTube API Key**: Über die Google Developer Console generieren.
- **Spotify API-Zugang**: Erstelle eine App auf [Spotify Developer](https://developer.spotify.com/dashboard/).

## Konfiguration
1. Installiere das Add-on in Home Assistant.
2. Konfiguriere folgende Optionen:
   - `DISCORD_TOKEN`: Dein Discord-Bot-Token.
   - `YOUTUBE_API_KEY`: Dein YouTube API Key.
   - `SPOTIFY_CLIENT_ID` und `SPOTIFY_CLIENT_SECRET`: Spotify Zugangsdaten.
3. Starte das Add-on.

## Ports
- Lavalink-Port: `2333/tcp`
