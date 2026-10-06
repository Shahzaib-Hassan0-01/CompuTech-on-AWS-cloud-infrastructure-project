# Security review: lab build vs. production

The lab was about getting things working inside AWS Academy's limits. This page is me reviewing my own build the way I'd review someone else's.

| # | Area | What I did in the lab | Risk | What I'd do in production |
|---|---|---|---|---|
| 1 | S3 | Public bucket policy (`Principal: "*"`) | Anyone can read every object; easy to leak something by accident | Keep bucket private, serve via **CloudFront + Origin Access Control**, HTTPS only |
| 2 | EC2 file permissions | `chmod 777` on `/var/www/html` | Web root writable by any user/process | Owner `ubuntu`, group `www-data`, dirs 755 / files 644 ([script](../ec2/deploy-permissions.sh)) |
| 3 | SSH | Port 22 open to `0.0.0.0/0` | Constant brute-force / scanning exposure | **SSM Session Manager**, no port 22; if SSH is required, allow only my IP |
| 4 | Web servers | Public IPs + port 80 open to the internet | Users can bypass the ALB | Instances in private subnets; SG allows 80 **only from the ALB's SG** |
| 5 | Transport | HTTP only | Traffic readable in transit | ALB HTTPS listener with **ACM** certificate, redirect 80 → 443 |
| 6 | RDS network | Publicly accessible, 3306 open | Database reachable from the internet | Private subnets, 3306 only from the app SG |
| 7 | RDS credentials | Self-managed, weak master password | Credential guessing / reuse | **Secrets Manager** with rotation, or IAM DB authentication |
| 8 | RDS resilience | Single-AZ, deletion protection off | Outage on AZ failure; accidental delete | Multi-AZ, deletion protection on |
| 9 | IAM | Broad shared `LabRole` for Lambda and Beanstalk | Far more permission than each workload needs | One role per workload, least privilege |
| 10 | Availability | All 5 ALB targets in one AZ | Single-AZ failure takes the site down | Targets spread across ≥ 2 AZs via an ASG |

Things that were already right: S3 default encryption (SSE-S3) and versioning on, ACLs disabled, RDS automated backups on, and the Workbench → RDS connection used TLS.
