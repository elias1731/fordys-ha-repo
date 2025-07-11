FROM php:8.2-apache

# Systempakete & Erweiterungen
RUN apt-get update && apt-get install -y \
    mariadb-server \
    supervisor \
    unzip \
    wget \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    && docker-php-ext-install mysqli pdo pdo_mysql

# YOURLS downloaden
ENV YOURLS_VERSION=1.9.2
RUN wget https://github.com/YOURLS/YOURLS/archive/refs/tags/${YOURLS_VERSION}.zip && \
    unzip ${YOURLS_VERSION}.zip && \
    mv YOURLS-${YOURLS_VERSION} /var/www/html/yourls && \
    rm ${YOURLS_VERSION}.zip

# Apache Config
RUN a2enmod rewrite

# Konfigurationen kopieren
COPY run.sh /run.sh
COPY supervisord.conf /etc/supervisord.conf
RUN chmod +x /run.sh

EXPOSE 8080

CMD ["/run.sh"]
