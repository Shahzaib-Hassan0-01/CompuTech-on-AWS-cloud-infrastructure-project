# Part 3 — Manual web server "CompuZilla" (EC2 + Apache + SFTP)

**Goal:** host the same CompuTech site on a single Linux VM, uploading files with FileZilla.

## Steps
1. Launched an Ubuntu 24.04 t3.micro named **CompuZilla** (SSH + HTTP allowed).
2. Connected with EC2 Instance Connect and installed Apache: `sudo apt install apache2 -y`. The public IP showed the Apache default page.
3. In FileZilla: SFTP, host = public IP, user `ubuntu`, logon type *Key file* (the `.pem` key pair).
4. Uploading into `/var/www/html` failed with **permission denied**: the folder is owned by `root`, and SFTP runs as `ubuntu`.
5. Fixed the permissions, re-uploaded, and the full site loaded from the instance's public IP.

![Site on CompuZilla](screenshots/03-ec2-website-live.png)

## What I'd do differently
In the lab I fixed step 4 with `sudo chmod 777` on the file and then the folder. It works, but it makes the web root **world-writable**: any user or compromised process on the box could change the site.

The least-privilege fix is in [`ec2/deploy-permissions.sh`](../ec2/deploy-permissions.sh): `ubuntu` owns the files so uploads work, and Apache (`www-data`) only gets read access (dirs `755`, files `644`).
