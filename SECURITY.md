# Security Considerations for Kraken

## Overview

Kraken is a penetration testing tool that discovers and logs credentials. This document outlines security considerations when deploying and using Kraken.

## Known Security Behaviors

### 1. Clear-Text Password Logging

**Status**: INTENTIONAL BEHAVIOR

Kraken logs discovered credentials in clear text. This is by design as the purpose of the tool is credential discovery.

**Locations:**
- Application logs (`kraken_auto.log`)
- Report files (`reports/*.json`)
- Telegram notifications

**Mitigation:**
```bash
# Restrict log file access
chmod 600 /opt/kraken/kraken_auto.log

# Restrict reports directory
chmod 700 /opt/kraken/reports/

# Regularly clean old reports
find /opt/kraken/reports/ -name "*.json" -mtime +7 -delete

# Use encrypted filesystem for sensitive directories
```

### 2. SSH Host Key Validation

**Status**: INTENTIONAL BEHAVIOR

The SSH brute force module uses `AutoAddPolicy` to accept any host key. This is necessary for automated scanning of unknown hosts and hidden services.

**Risk**: Man-in-the-middle attacks

**Mitigation:**
- Only scan on trusted networks or through Tor
- Hidden services provide cryptographic guarantees about identity
- This is standard for automated penetration testing tools

### 3. Tor Usage

**Status**: RECOMMENDED

When scanning hidden services, all traffic goes through Tor SOCKS proxy.

**Security Considerations:**
- Tor provides anonymity but not encryption beyond the Tor network
- Ensure Tor is properly configured
- Keep Tor daemon updated

**Verification:**
```bash
# Check Tor is running
sudo systemctl status tor

# Verify SOCKS proxy
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org
```

### 4. Telegram Bot Security

**Credentials in Configuration**: Bot tokens and chat IDs are stored in `config.json`

**Protection:**
```bash
# Restrict config file access
chmod 600 /opt/kraken/config.json

# Never commit config.json to version control
# Use config.example.json as template
```

**Bot Security Best Practices:**
- Use dedicated bot for Kraken only
- Revoke bot token if compromised
- Use private chat (not groups)
- Regularly review bot messages for unexpected activity

## Deployment Security

### File Permissions

```bash
# Set restrictive permissions on installation
sudo chown -R root:root /opt/kraken
sudo chmod 700 /opt/kraken
sudo chmod 600 /opt/kraken/config.json
sudo chmod 600 /opt/kraken/hidden_services.json
sudo chmod 700 /opt/kraken/reports
```

### Systemd Service Hardening

The provided systemd service includes:
- `PrivateTmp=yes` - Isolated /tmp directory
- `NoNewPrivileges=true` - Prevents privilege escalation
- `ReadWritePaths` - Restricted write access

### Network Security

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh

# Only allow local Tor SOCKS access
sudo ufw allow from 127.0.0.1 to any port 9050
```

### VPS Hardening

1. **Keep System Updated:**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Disable Root SSH Login:**
```bash
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd
```

3. **Use SSH Keys Only:**
```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
```

4. **Install Fail2Ban:**
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

## Data Protection

### Encrypt Sensitive Directories

```bash
# Use LUKS encryption for reports directory
sudo apt install cryptsetup

# Create encrypted volume
sudo cryptsetup luksFormat /dev/vdb
sudo cryptsetup open /dev/vdb kraken_reports

# Format and mount
sudo mkfs.ext4 /dev/mapper/kraken_reports
sudo mount /dev/mapper/kraken_reports /opt/kraken/reports
```

### Secure Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/kraken
```

```
/opt/kraken/kraken_auto.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0600 root root
    shred
}

/var/log/kraken/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0600 root root
    shred
}
```

## Incident Response

### If System is Compromised

1. **Stop Kraken immediately:**
```bash
sudo systemctl stop kraken.timer
sudo systemctl stop kraken.service
```

2. **Secure or delete sensitive data:**
```bash
# Backup reports if needed
tar -czf kraken_reports_backup.tar.gz /opt/kraken/reports/
# Securely delete
sudo shred -vfz -n 10 /opt/kraken/reports/*.json
sudo shred -vfz -n 10 /opt/kraken/kraken_auto.log
```

3. **Revoke Telegram bot:**
- Contact @BotFather
- Use `/revoke` command
- Generate new bot token

4. **Investigate:**
```bash
# Check system logs
sudo journalctl -u kraken.service -n 1000
sudo last
sudo lastb
```

### If Credentials are Leaked

1. **Identify affected systems** from reports
2. **Change all discovered passwords**
3. **Review access logs** on affected systems
4. **Implement additional security measures**

## Compliance and Legal

### Scope of Authorization

⚠️ **CRITICAL**: Only scan systems you own or have explicit written permission to test.

### Logging Requirements

- Maintain logs of scan activities
- Document authorization for all targets
- Keep records of discovered credentials separately
- Implement audit trails

### Data Retention

```bash
# Automatically delete old reports (30 days)
echo "0 0 * * * find /opt/kraken/reports/ -name '*.json' -mtime +30 -delete" | sudo crontab -
```

## Monitoring and Alerting

### Monitor Kraken Activity

```bash
# Watch logs in real-time
tail -f /opt/kraken/kraken_auto.log

# Check systemd service status
watch -n 60 'systemctl status kraken.service'

# Monitor disk usage
du -sh /opt/kraken/reports/
```

### Alert on Anomalies

Set up monitoring for:
- Unusual scan frequency
- Unexpected target additions
- Large number of failed scans
- Unusual network traffic patterns

## Secure Decommissioning

When retiring a Kraken installation:

```bash
# Stop services
sudo systemctl stop kraken.timer
sudo systemctl disable kraken.timer
sudo systemctl stop kraken.service
sudo systemctl disable kraken.service

# Securely delete data
sudo shred -vfz -n 10 /opt/kraken/config.json
sudo shred -vfz -n 10 /opt/kraken/hidden_services.json
find /opt/kraken/reports/ -type f -exec shred -vfz -n 10 {} \;

# Remove installation
sudo rm -rf /opt/kraken

# Remove systemd files
sudo rm /etc/systemd/system/kraken.service
sudo rm /etc/systemd/system/kraken.timer
sudo systemctl daemon-reload
```

## Responsible Disclosure

If you discover security vulnerabilities in Kraken:

1. Do NOT disclose publicly
2. Contact the maintainer privately
3. Provide detailed information
4. Allow reasonable time for fixes

## Summary

Kraken is a powerful penetration testing tool that requires careful security considerations:

✅ **Do:**
- Secure all logs and reports with strict permissions
- Use encrypted storage for sensitive data
- Regularly review and clean old data
- Harden the VPS environment
- Only scan authorized targets
- Monitor for suspicious activity

❌ **Don't:**
- Leave reports world-readable
- Commit config files to version control
- Scan unauthorized systems
- Share Telegram bot tokens
- Ignore security updates
- Run as non-root without proper considerations

---

**Last Updated**: 2023-11-13

**Remember**: With great power comes great responsibility. Use Kraken ethically and legally.
