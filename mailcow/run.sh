#!/bin/bash
echo "Starte Mailcow innerhalb des Add-ons..."

# Sicherstellen, dass Docker läuft
service docker start

# Mailcow Umgebung konfigurieren
if [ ! -f "/mailcow/mailcow.conf" ]; then
  cp /mailcow/mailcow.conf.example /mailcow/mailcow.conf
  echo "Mailcow wurde initialisiert. Bitte konfiguriere die mailcow.conf!"
fi

# Docker Compose starten
docker-compose up -d

# Halte den Container am Laufen
tail -f /dev/null
