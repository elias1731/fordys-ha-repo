FROM debian:bullseye

# System vorbereiten
RUN apt-get update && apt-get install -y \
    curl git docker.io docker-compose \
    && apt-get clean

# Mailcow klonen
RUN git clone https://github.com/mailcow/mailcow-dockerized /mailcow

# Arbeitsverzeichnis setzen
WORKDIR /mailcow

# Skript zum Starten
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]