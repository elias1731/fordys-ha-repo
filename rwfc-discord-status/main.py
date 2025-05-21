import asyncio
import os
import json
import logging
import discord # discord.py Bibliothek
import aiohttp

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfiguration aus Umgebungsvariablen laden
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
HA_SENSOR_ENTITY_ID = os.getenv('SENSOR_ENTITY_ID')
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 60))
ACTIVITY_TYPE_STR = os.getenv('ACTIVITY_TYPE_STR', 'playing').lower()
STATUS_TEMPLATE = os.getenv('STATUS_TEMPLATE', '{state}') # Standardvorlage

HA_TOKEN = os.getenv('SUPERVISOR_TOKEN')
HA_API_BASE_URL = "http://supervisor/core/api"

# Discord Activity Type Mapping
activity_type_map = {
    "playing": discord.ActivityType.playing,
    "watching": discord.ActivityType.watching,
    "listening": discord.ActivityType.listening,
    "streaming": discord.ActivityType.streaming, # Benötigt eine stream_url
    "competing": discord.ActivityType.competing,
}
SELECTED_ACTIVITY_TYPE = activity_type_map.get(ACTIVITY_TYPE_STR, discord.ActivityType.playing)

intents = discord.Intents.default()
# Keine speziellen Intents für reines Status-Update nötig, aber Presence Intent ist im Developer Portal zu aktivieren.
client = discord.Client(intents=intents)
last_known_state_str = None

async def get_ha_sensor_state(session, entity_id):
    """Ruft den Zustand eines Sensors von der Home Assistant API ab."""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    url = f"{HA_API_BASE_URL}/states/{entity_id}"
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            logger.info(f"Sensor-Daten für {entity_id} empfangen: {data.get('state')}")
            return data.get('state'), data.get('attributes', {})
    except aiohttp.ClientError as e:
        logger.error(f"Fehler beim Abrufen des Sensorstatus von Home Assistant für {entity_id}: {e}")
        return None, {}
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim Abrufen des Sensorstatus für {entity_id}: {e}")
        return None, {}

def format_status(template: str, state: str, attributes: dict) -> str:
    """Formatiert den Status-String basierend auf der Vorlage, dem Zustand und den Attributen."""
    status_text = template.replace("{state}", str(state))
    # Ersetze Attribute, z.B. {attributes.friendly_name}
    for key, value in attributes.items():
        status_text = status_text.replace(f"{{attributes.{key}}}", str(value))
    return status_text

async def update_bot_status():
    """Aktualisiert den Discord Bot Status basierend auf dem Sensorzustand."""
    global last_known_state_str
    if not client.is_ready():
        logger.warning("Discord Client ist nicht bereit. Überspringe Status-Update.")
        return

    async with aiohttp.ClientSession() as session:
        current_state_value, attributes = await get_ha_sensor_state(session, HA_SENSOR_ENTITY_ID)

    if current_state_value is None:
        logger.warning("Konnte Sensorstatus nicht abrufen. Überspringe Discord Update.")
        # Optional: Status löschen oder Fehlermeldung anzeigen
        # await client.change_presence(activity=None)
        return

    # Formatiere den Status-String
    status_display_text = format_status(STATUS_TEMPLATE, current_state_value, attributes)

    # Nur aktualisieren, wenn sich der formatierte Status geändert hat
    if status_display_text == last_known_state_str:
        logger.info(f"Sensorstatus ('{status_display_text}') unverändert. Überspringe Discord Update.")
        return

    activity_name = status_display_text
    activity = discord.Activity(name=activity_name, type=SELECTED_ACTIVITY_TYPE)

    # Für Streaming-Typ wird eine URL benötigt
    if SELECTED_ACTIVITY_TYPE == discord.ActivityType.streaming:
        # Du könntest eine Konfigurationsoption für die Stream-URL hinzufügen
        # Hier als Beispiel eine statische URL, die du anpassen müsstest
        stream_url = attributes.get("stream_url", "https://www.twitch.tv/homeassistant")
        activity = discord.Streaming(name=activity_name, url=stream_url)

    try:
        await client.change_presence(activity=activity)
        last_known_state_str = status_display_text
        logger.info(f"Discord Bot Status erfolgreich aktualisiert auf: [{ACTIVITY_TYPE_STR}] {activity_name}")
    except discord.DiscordException as e:
        logger.error(f"Fehler beim Aktualisieren des Discord Bot Status: {e}")
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim Aktualisieren des Discord Bot Status: {e}")

@client.event
async def on_ready():
    logger.info(f'Bot erfolgreich eingeloggt als {client.user.name} (ID: {client.user.id})')
    logger.info('------------------------------------------------------')
    # Erstes Update direkt nach dem Verbinden
    await update_bot_status()

async def main_loop():
    """Hauptschleife, die periodisch den Status prüft und aktualisiert."""
    while True:
        if client.is_ready(): # Nur wenn der Bot verbunden ist
            await update_bot_status()
        else:
            logger.warning("Warte darauf, dass der Discord Client bereit ist...")
        await asyncio.sleep(UPDATE_INTERVAL)

async def start_bot():
    if not BOT_TOKEN:
        logger.error("Discord Bot Token nicht gefunden. Bitte in der Addon-Konfiguration setzen.")
        return
    if not HA_SENSOR_ENTITY_ID:
        logger.error("Sensor Entity ID nicht gefunden. Bitte in der Addon-Konfiguration setzen.")
        return
    if not HA_TOKEN:
        logger.error("Home Assistant Supervisor Token nicht gefunden.")
        return

    logger.info("Starte Discord Bot Status Addon...")
    logger.info(f"Überwachter Sensor: {HA_SENSOR_ENTITY_ID}")
    logger.info(f"Update Intervall: {UPDATE_INTERVAL}s")
    logger.info(f"Activity Typ: {ACTIVITY_TYPE_STR}")
    logger.info(f"Status Vorlage: '{STATUS_TEMPLATE}'")

    try:
        # Starte den Bot und die Hauptschleife parallel
        # Die discord.py Bibliothek blockiert, wenn client.start() aufgerufen wird.
        # Daher muss die periodische Aktualisierung in einer Hintergrundaufgabe laufen,
        # die von discord.py's Event-Schleife verwaltet wird.
        # Alternativ könnte man client.loop.create_task(main_loop()) verwenden,
        # nachdem der Bot sich verbunden hat (innerhalb von on_ready).
        async def runner():
            await client.login(BOT_TOKEN)
            # Warte bis on_ready gefeuert wurde und der Client wirklich bereit ist.
            await client.wait_until_ready()
            # Starte die periodische Update-Schleife als Hintergrundtask
            client.loop.create_task(main_loop())
            await client.connect(reconnect=True)

        await runner()

    except discord.LoginFailure:
        logger.error("Login zum Discord Bot fehlgeschlagen. Überprüfe das Bot Token.")
    except Exception as e:
        logger.error(f"Ein Fehler ist beim Starten des Bots aufgetreten: {e}")
    finally:
        if client.is_ready():
            await client.close()
        logger.info("Discord Bot Status Addon gestoppt.")


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Addon durch Benutzer gestoppt.")
    except Exception as e:
        logger.critical(f"Kritischer Fehler in der Hauptausführung: {e}", exc_info=True)
