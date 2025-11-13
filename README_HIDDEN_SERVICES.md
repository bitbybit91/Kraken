# Kraken - Hidden Services Automated Scanner

This version of Kraken is specifically designed for Ubuntu VPS environments to automatically scan hidden services (.onion sites) with full Tor support, Telegram notifications, and automated execution via systemd.

## Features

- **Tor/Hidden Service Support**: Full support for .onion domains via SOCKS5 proxy
- **Telegram Notifications**: Real-time notifications when credentials are found
- **Automated Execution**: Systemd service runs automatically every 2 hours
- **Structured Reporting**: All results saved in JSON format with timestamps
- **Production Ready**: Error handling, logging, and security hardening
- **No User Interaction**: Fully automated operation suitable for VPS deployment

## Installation

### Quick Install

Run the installation script as root:

```bash
sudo bash install.sh
```

The installer will:
1. Install system dependencies (Python 3, Tor, pip)
2. Install Python dependencies
3. Configure Tor
4. Install Kraken to `/opt/kraken`
5. Setup systemd service and timer
6. Configure Telegram notifications (optional)

### Manual Installation

1. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip tor git
pip3 install -r requirements.txt
pip3 install PySocks
```

2. Configure Tor:
```bash
sudo systemctl enable tor
sudo systemctl start tor
```

3. Copy files to `/opt/kraken`:
```bash
sudo mkdir -p /opt/kraken
sudo cp -r ./* /opt/kraken/
```

4. Install systemd service:
```bash
sudo cp kraken.service /etc/systemd/system/
sudo cp kraken.timer /etc/systemd/system/
sudo systemctl daemon-reload
```

## Configuration

### 1. Configure Hidden Services Targets

Edit `hidden_services.json`:

```json
{
  "hidden_services": [
    {
      "name": "target_service",
      "url": "http://example.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": true,
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    }
  ]
}
```

**Supported service types:**
- `wordpress` - WordPress sites
- `ssh` - SSH servers

### 2. Configure Telegram Notifications (Optional)

Edit `config.json`:

```json
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID",
    "enabled": true
  }
}
```

**How to get Telegram credentials:**
1. Create a bot with [@BotFather](https://t.me/botfather)
2. Get your Chat ID from [@userinfobot](https://t.me/userinfobot)

### 3. Configure Tor Settings

The default Tor configuration in `config.json`:

```json
{
  "tor": {
    "socks_proxy": "socks5h://127.0.0.1:9050",
    "enabled": true
  }
}
```

## Usage

### Automated Mode (Recommended)

Start the timer to run Kraken every 2 hours:

```bash
sudo systemctl enable kraken.timer
sudo systemctl start kraken.timer
```

Check timer status:
```bash
systemctl status kraken.timer
systemctl list-timers kraken.timer
```

### Manual Mode

Run Kraken once:

```bash
cd /opt/kraken
python3 kraken_auto.py
```

### Stop/Disable Automated Scanning

```bash
sudo systemctl stop kraken.timer
sudo systemctl disable kraken.timer
```

## Reports

All findings are saved to `/opt/kraken/reports/` in JSON format:

```
/opt/kraken/reports/
├── target_service_20231113_142530.json
├── another_target_20231113_143045.json
└── ...
```

Each report contains:
- Timestamp
- Target URL/Host
- Username
- Password
- Service type
- Additional metadata

Example report:
```json
{
  "timestamp": "2023-11-13T14:25:30.123456",
  "target": "http://example.onion",
  "username": "admin",
  "password": "password123",
  "service_type": "wordpress"
}
```

## Logs

### Application Logs

- **Main log**: `/opt/kraken/kraken_auto.log`
- **Systemd logs**: `/var/log/kraken/kraken.log` and `/var/log/kraken/kraken_error.log`

View logs:
```bash
# Main application log
tail -f /opt/kraken/kraken_auto.log

# Systemd logs
tail -f /var/log/kraken/kraken.log

# All systemd logs for the service
journalctl -u kraken.service -f
```

## Telegram Notifications

When enabled, you'll receive:

### Scan Started
```
🔍 Kraken - Scan Started
⏰ Time: 2023-11-13 14:25:30
🌐 Service: target_service
🔗 URL: http://example.onion
```

### Credentials Found
```
🎯 Kraken - Credentials Found
⏰ Time: 2023-11-13 14:30:15
🌐 Service: target_service
🔗 URL: http://example.onion
👤 Username: admin
🔑 Password: password123
📋 Additional Info:
   • type: WordPress
```

### Scan Completed
```
✅ Kraken - Scan Completed
⏰ Time: 2023-11-13 14:35:00
🌐 Service: target_service
📊 Results: 2 credential(s) found
```

## Wordlists

Place your wordlists in the `wordlists/` directory:

```
wordlists/
├── users.txt          # Common usernames
├── passwords.txt      # Common passwords
├── users_custom.txt   # Custom usernames
└── passwords_custom.txt # Custom passwords
```

Reference them in `hidden_services.json`:
```json
"wordlists": {
  "users": "wordlists/users_custom.txt",
  "passwords": "wordlists/passwords_custom.txt"
}
```

## Security Considerations

### System Hardening

The systemd service includes security hardening:
- `PrivateTmp=yes` - Isolated /tmp directory
- `NoNewPrivileges=true` - Prevents privilege escalation
- `ReadWritePaths` - Restricted write access

### Tor Configuration

Ensure Tor is properly configured:
```bash
# Check Tor status
sudo systemctl status tor

# Test Tor connection
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org
```

### Firewall

Configure UFW to allow only necessary connections:
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow from 127.0.0.1 to any port 9050  # Tor SOCKS
```

## Troubleshooting

### Tor Connection Issues

1. Check Tor status:
```bash
sudo systemctl status tor
```

2. Restart Tor:
```bash
sudo systemctl restart tor
```

3. Verify SOCKS proxy:
```bash
netstat -tlnp | grep 9050
```

### Service Not Running

1. Check service status:
```bash
sudo systemctl status kraken.service
sudo systemctl status kraken.timer
```

2. View error logs:
```bash
sudo journalctl -u kraken.service -n 50
```

3. Test manually:
```bash
cd /opt/kraken
sudo python3 kraken_auto.py
```

### Telegram Not Working

1. Verify bot token and chat ID in `config.json`
2. Test Telegram API:
```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/getMe"
```

### No Results Found

1. Verify target is accessible:
```bash
# For .onion sites
torify curl http://example.onion

# For SSH
torify nc -zv example.onion 22
```

2. Check wordlists exist and are readable
3. Review logs for errors

## Maintenance

### Update Kraken

```bash
cd /home/user/Kraken  # Original clone location
git pull
sudo bash install.sh
sudo systemctl restart kraken.timer
```

### Clean Old Reports

```bash
# Remove reports older than 30 days
find /opt/kraken/reports/ -name "*.json" -mtime +30 -delete
```

### Backup Configuration

```bash
# Backup configs and wordlists
tar -czf kraken_backup.tar.gz /opt/kraken/config.json /opt/kraken/hidden_services.json /opt/kraken/wordlists/
```

## Advanced Configuration

### Custom Settings

Edit `config.json` to customize:

```json
{
  "settings": {
    "threads": 10,        // Concurrent threads
    "timeout": 30,        // Connection timeout (seconds)
    "reports_dir": "reports",  // Reports directory
    "auto_mode": true     // Enable automated mode
  }
}
```

### Change Timer Interval

Edit `/etc/systemd/system/kraken.timer`:

```ini
[Timer]
OnBootSec=5min       # First run after 5 minutes of boot
OnUnitActiveSec=2h   # Run every 2 hours (change as needed)
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart kraken.timer
```

## Legal Disclaimer

⚠️ **WARNING**: This tool is for educational and authorized testing purposes only.

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- The author is not responsible for misuse of this tool
- Users are solely responsible for their actions

## Support

For issues or questions:
1. Check the logs
2. Review this documentation
3. Open an issue on GitHub

## License

See the main README.md for license information.
