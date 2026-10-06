#!/bin/bash
# EC2 user data (runs once, as root, on first boot) for Ubuntu 24.04.
# Installs Apache + PHP and serves a page showing which server answered.
# Used for the Auto Scaling Group launch template (Part 2) and the
# five ALB target instances (Part 4). Change SERVER_LABEL per instance.

SERVER_LABEL="Web Server #1"

apt-get update -y
apt-get install -y apache2 php libapache2-mod-php

rm -f /var/www/html/index.html
cat > /var/www/html/index.php <<HTML
<html>
  <body>
    <p>${SERVER_LABEL}</p>
    <p>Bringing Digital Technologies to an Analog World!</p>
    <p>Hostname: <?php echo gethostname(); ?></p>
  </body>
</html>
HTML

systemctl enable --now apache2
