#!/usr/bin/env bash
set -e

# Platzhalter ersetzen durch HA options
CONFIG_PATH=/data/options.json
ADMIN_USER=$(jq -r '.admin_user' "$CONFIG_PATH")
ADMIN_PASSWORD=$(jq -r '.admin_password' "$CONFIG_PATH")

# Auf MariaDB-Datenverzeichnis prüfen
if [ ! -d "/var/lib/mysql/yourls" ]; then
    echo "[INFO] Initialisiere MariaDB-Datenbank..."
    mysql_install_db > /dev/null
    mysqld_safe --skip-networking &
    sleep 5

    mysql -e "CREATE DATABASE yourls;"
    mysql -e "CREATE USER 'yourls'@'localhost' IDENTIFIED BY 'yourls';"
    mysql -e "GRANT ALL PRIVILEGES ON yourls.* TO 'yourls'@'localhost';"
    mysql -e "FLUSH PRIVILEGES;"
    killall mysqld
    sleep 5
fi

# YOURLS config.php generieren
cat <<EOF > /var/www/html/yourls/user/config.php
<?php
define('YOURLS_DB_USER', 'yourls');
define('YOURLS_DB_PASS', 'yourls');
define('YOURLS_DB_NAME', 'yourls');
define('YOURLS_DB_HOST', '127.0.0.1');
define('YOURLS_SITE', 'http://localhost:8080/yourls');
define('YOURLS_HOURS_OFFSET', 0);
define('YOURLS_LANG', '');
define('YOURLS_UNIQUE_URLS', true);
\$yourls_user_passwords = array(
  '$ADMIN_USER' => '$ADMIN_PASSWORD',
);
define('YOURLS_PRIVATE', true);
define('YOURLS_COOKIEKEY', '$(head -c 64 /dev/urandom | base64)');
?>
EOF

chown -R www-data:www-data /var/www/html/yourls

# Supervisor starten (Apache + MariaDB)
exec supervisord -c /etc/supervisord.conf
