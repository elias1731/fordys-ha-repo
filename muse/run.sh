#!/usr/bin/env bash

# Überprüfen, ob alle Umgebungsvariablen gesetzt sind
if [ -z "$DISCORD_TOKEN" ]; then
  echo "Fehler: DISCORD_TOKEN ist nicht gesetzt."
  exit 1
fi

# Docker Compose starten
docker-compose up -d
