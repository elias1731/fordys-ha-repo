#!/usr/bin/with-contenv bashio

bashio::log.info "Starting Discord Bot Status Addon"

# Hole Konfiguration
CONFIG_PATH=/data/options.json
DISCORD_BOT_TOKEN=$(bashio::config 'discord_bot_token')
SENSOR_ENTITY_ID=$(bashio::config 'sensor_entity_id')
UPDATE_INTERVAL=$(bashio::config 'update_interval')
ACTIVITY_TYPE_STR=$(bashio::config 'activity_type')
STATUS_TEMPLATE=$(bashio::config 'status_template')

# Exportiere Variablen für das Python-Skript
export DISCORD_BOT_TOKEN
export SENSOR_ENTITY_ID
export UPDATE_INTERVAL
export ACTIVITY_TYPE_STR
export STATUS_TEMPLATE
export SUPERVISOR_TOKEN=${SUPERVISOR_TOKEN} # Wichtig für HA API Zugriff

# Starte das Python-Skript
python3 /main.py
