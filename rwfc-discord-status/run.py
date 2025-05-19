import time
import json
import requests
from pypresence import Presence
import os

# Load options from Home Assistant
OPTIONS_PATH = "/data/options.json"
with open(OPTIONS_PATH, "r") as f:
    config = json.load(f)

client_id = config["discord_client_id"]
fc1 = config["fc1"]
fc2 = config["fc2"]
api_url = config["api_url"]

# Mapping der Raumtypen
ROOM_NAMES = {
    "vs_10": "🕹️ Retro VS",
    "vs_11": "⏰ Retro ZF",
    "vs_12": "🚀 Retro 200cc",
    "vs_20": "🚧 Custom VS",
    "vs_21": "⏰ Custom ZF",
    "vs_22": "💥 Custom 200cc",
    "vs_668": "🏁 CTGP-C",
    "vs_69": "🏁 Insane Kart",
    "vs_-1": "🚗 Standard",
    "vs": "🚗 Standard",
    "vs_666": "Luminous"
}

def fetch_data():
    try:
        res = requests.get(api_url, timeout=5)
        res.raise_for_status()
        return res.json()
    except:
        return []

def get_status_for_fc(data, fc):
    for session in data:
        if "players" in session and isinstance(session["players"], dict):
            for player_data in session["players"].values():
                if player_data.get("fc") == fc:
                    rk = session.get("rk", "unknown")
                    count = len(session["players"])
                    name = ROOM_NAMES.get(rk, rk)
                    suffix = f"(voll!)" if count >= 12 else f"({count} Spieler)"
                    return rk, name, count, suffix
    return None, "🚫 OFFLINE", 0, ""

def build_presence(data):
    status1 = get_status_for_fc(data, fc1)
    status2 = get_status_for_fc(data, fc2)

    if status1[0] != "unknown" and status1[0] != None and status1[0] == status2[0]:
        return {
            "details": f"{fc1} & {fc2} gemeinsam",
            "state": f"{status1[1]} +{status1[2]-2} weitere",
        }
    elif status1[1] != "🚫 OFFLINE":
        return {
            "details": f"{fc1} online",
            "state": f"{status1[1]} {status1[3]}",
        }
    elif status2[1] != "🚫 OFFLINE":
        return {
            "details": f"{fc2} online",
            "state": f"{status2[1]} {status2[3]}",
        }
    else:
        return {
            "details": "Keiner online",
            "state": "🚫 OFFLINE",
        }

# Start Discord RPC
rpc = Presence(client_id)
rpc.connect()

while True:
    try:
        data = fetch_data()
        presence = build_presence(data)
        rpc.update(
            details=presence["details"],
            state=presence["state"],
            large_image="mkwii",
            large_text="Mario Kart Wii",
            small_image="online" if "online" in presence["details"].lower() else "offline"
        )
    except Exception as e:
        print("Fehler:", e)

    time.sleep(10)
