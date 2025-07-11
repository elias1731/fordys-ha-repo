#!/usr/bin/env bash
set -e

# MySQL starten
service mysql start

# DB & User vorbereiten
mysql -e "CREATE DATABASE IF NOT EXISTS yourls;"
mysql -e "CREATE USER IF NOT EXISTS 'yourls'@'localhost' IDENTIFIED BY 'yourls';"
mysql -e "GRANT ALL PRIVILEGES ON yourls.* TO 'yourls'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# YOURLS config.php generieren
cat <<EOF > /var/www/html/yourls/user/config.php
<?php
define('YOURLS_DB_USER', 'yourls');
define('YOURLS_DB_PASS', 'yourls');
define('YOURLS_DB_NAME', 'yourls');
define('YOURLS_DB_HOST', 'localhost');
define('YOURLS_SITE', 'http://localhost:8080/yourls');
define('YOURLS_HOURS_OFFSET', 0);
define('YOURLS_LANG', '');
define('YOURLS_UNIQUE_URLS', true);
\$yourls_user_passwords = array(
  '${ADMIN_USER}' => '${ADMIN_PASSWORD}',
);
define('YOURLS_PRIVATE', true);
define('YOURLS_COOKIEKEY', '$(head -c 64 /dev/urandom | base64)');
?>
EOF

# Rechte fixen
chown -R www-data:www-data /var/www/html/yourls

# Apache starten
exec apache2-foreground
