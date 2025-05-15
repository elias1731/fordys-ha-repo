#!/bin/bash

# Starte PostgreSQL
service postgresql start

# Warte kurz, damit die DB bereit ist
sleep 3

# Erstelle DB & Nutzer falls nötig
sudo -u postgres psql -c "CREATE USER wfc WITH PASSWORD 'wfcpass';" || true
sudo -u postgres psql -c "CREATE DATABASE wfc OWNER wfc;" || true

# Starte den WFC-Server
cd /opt/wfc-server
./wfc-server