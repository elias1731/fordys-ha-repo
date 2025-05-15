FROM golang:1.21-bullseye

RUN apt-get update &&     apt-get install -y git postgresql postgresql-contrib

# Klone den WFC-Server von WiiLink
RUN git clone https://github.com/WiiLink24/wfc-server /opt/wfc-server

WORKDIR /opt/wfc-server

# Baue den Server
RUN go build -o wfc-server main.go

# Kopiere Startskript
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]