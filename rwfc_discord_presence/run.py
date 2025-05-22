from pypresence import Presence
import time
import requests
import os
import json

CONFIG_PATH = "/data/options.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_sensor_state(cfg):
    url = f"{cfg['ha_url']}/api/states/{cfg['sensor_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['ha_token']}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["state"], data.get("attributes", {}).get("friendly_name", cfg["sensor_id"])
    except Exception as e:
        print(f"[Fehler beim Abrufen des Sensors] {e}")
        return None, None

def main():
    cfg = load_config()
    rpc = Presence(cfg["discord_app_id"])
    rpc.connect()
    last_state = None

    try:
        while True:
            state, name = get_sensor_state(cfg)
            if state and state != last_state:
                rpc.update(
                    details=f"{name}",
                    state=f"Status: {state}",
                    large_image="retrorewind",  # Optional: Bildname in Discord App Assets
                    large_text="Mario Kart Wii: RetroRewind"
                )
                print(f"[Update] {name}: {state}")
                last_state = state
            elif not state:
                rpc.clear()
                last_state = None
                print("[Status gelöscht]")
            time.sleep(10)
    except KeyboardInterrupt:
        rpc.clear()
        rpc.close()

if __name__ == "__main__":
    main()