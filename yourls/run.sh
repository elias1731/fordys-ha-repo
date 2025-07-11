#!/usr/bin/env bash
set -e

CONFIG_PATH=/data/options.json
ADMIN_USER=$(jq -r '.admin_user' "$CONFIG_PATH")
ADMIN_PASSWORD=$(jq -r '.admin_password' "$CONFIG_PATH")

echo "[INFO] ADMIN_USER: $ADMIN_USER"

# Datenbank initialisieren falls leer
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "[INFO] Initialisiere MariaDB Datenbank..."
    mysqld --initialize-insecure --user=mysql
fi

# YOURLS Konfiguration schreiben
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

# Besitzrechte setzen
chown -R www-data:www-data /var/www/html/yourls

# Start via supervisord (Apache & MySQL)
exec supervisord -c /etc/supervisord.conf