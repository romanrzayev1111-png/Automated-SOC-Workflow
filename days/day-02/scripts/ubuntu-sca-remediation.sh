#!/bin/bash
# Transcribed from WEEK2.docx image55; run only after reviewing this host's policy.
# The original mode backups below are overwritten on a second run.
set -euo pipefail

echo "===== BEFORE REMEDIATION ====="
stat -c '%a %U:%G %n' /etc/crontab /etc/cron.hourly

# Original permissions for rollback (modes only, not a full file/owner backup).
stat -c '%a' /etc/crontab > /root/crontab.perm.bak
stat -c '%a' /etc/cron.hourly > /root/cron.hourly.perm.bak

echo "===== APPLYING HARDENING ====="
chown root:root /etc/crontab /etc/cron.hourly
chmod 600 /etc/crontab
chmod 700 /etc/cron.hourly

echo "===== AFTER REMEDIATION ====="
stat -c '%a %U:%G %n' /etc/crontab /etc/cron.hourly
echo "SCA remediation completed."
