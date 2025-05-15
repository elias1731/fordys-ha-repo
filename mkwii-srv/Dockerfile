FROM python:3.11-slim

RUN apt-get update && apt-get install -y git &&     pip install --no-cache-dir dnslib flask

RUN git clone https://github.com/leseratte10/wiimmfi-private-server /app

WORKDIR /app

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]