#!/bin/bash
# Run on the "CompuZilla" EC2 instance before uploading the site with
# FileZilla (SFTP as the "ubuntu" user).
#
# In the original lab I used `chmod 777` to get past "permission denied".
# That works, but it makes the web root writable by every user and process
# on the box. This is the least-privilege version:
#   - ubuntu owns the files, so SFTP uploads work
#   - Apache (www-data) only gets read access, which is all it needs

set -e
WEB_ROOT=/var/www/html

sudo chown -R ubuntu:www-data "$WEB_ROOT"
sudo find "$WEB_ROOT" -type d -exec chmod 755 {} \;
sudo find "$WEB_ROOT" -type f -exec chmod 644 {} \;

ls -la "$WEB_ROOT"
