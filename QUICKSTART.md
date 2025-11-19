# Kraken Hidden Services - Quick Start Guide

Get Kraken running on your Ubuntu VPS in under 5 minutes!

## Prerequisites

- Ubuntu 18.04+ VPS with root access
- Internet connection
- (Optional) Telegram account for notifications

## Installation

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/bitbybit91/Kraken.git
cd Kraken

# Run installer as root
sudo bash install.sh
```

The installer will:
- Install Python 3, Tor, and dependencies
- Configure Tor for SOCKS proxy
- Install Kraken to `/opt/kraken`
- Setup systemd service
- Configure Telegram (optional)

### 2. Configure Targets

Edit the hidden services configuration:

```bash
sudo nano /opt/kraken/hidden_services.json
```

Add your targets:

```json
{
  "hidden_services": [
    {
      "name": "target_wordpress",
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

**Important**: Set `"enabled": true` for targets you want to scan!

**📖 Need help adding SSH, FTP, or other services? See [ADDING_SERVICES.md](ADDING_SERVICES.md)**

### 3. Configure Telegram (Optional)

If you want Telegram notifications:

1. Create a bot with [@BotFather](https://t.me/botfather)
   - Send `/newbot` and follow instructions
   - Save the bot token

2. Get your Chat ID from [@userinfobot](https://t.me/userinfobot)
   - Send `/start` to get your ID

3. Update config:

```bash
sudo nano /opt/kraken/config.json
```

```json
{
  "telegram": {
    "bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    "chat_id": "123456789",
    "enabled": true
  }
}
```

### 4. Start Kraken

**Option A: Automated (Runs every 2 hours)**

```bash
sudo systemctl enable kraken.timer
sudo systemctl start kraken.timer
```

**Option B: Run Once**

```bash
cd /opt/kraken
sudo python3 kraken_auto.py
```

## Verify It's Working

### Check Timer Status

```bash
systemctl status kraken.timer
systemctl list-timers kraken.timer
```

### View Logs

```bash
# Real-time logs
tail -f /opt/kraken/kraken_auto.log

# Systemd logs
sudo journalctl -u kraken.service -f
```

### Check Reports

```bash
ls -la /opt/kraken/reports/
```

## Test Tor Connection

Verify Tor is working:

```bash
# Check Tor is running
sudo systemctl status tor

# Test Tor connection
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org | grep Congratulations
```

## What Happens When Running?

1. **Scan Start**: Kraken reads targets from `hidden_services.json`
2. **Tor Connection**: Connects through Tor SOCKS proxy (127.0.0.1:9050)
3. **Service Detection**: Validates target is accessible
4. **Brute Force**: Tests credentials from wordlists
5. **Results**: Saves findings to `/opt/kraken/reports/`
6. **Telegram**: Sends notifications if enabled

## Example Workflow

```bash
# 1. View current configuration
cat /opt/kraken/hidden_services.json

# 2. Check if any targets are enabled
grep -A 5 '"enabled": true' /opt/kraken/hidden_services.json

# 3. Run a manual scan
cd /opt/kraken
sudo python3 kraken_auto.py

# 4. Check results
ls -lh /opt/kraken/reports/

# 5. View latest report
cat /opt/kraken/reports/*.json | tail -20
```

## Common Issues

### Tor Not Working

```bash
# Restart Tor
sudo systemctl restart tor

# Check Tor logs
sudo journalctl -u tor -n 50
```

### No Results

1. Check if targets are enabled in `hidden_services.json`
2. Verify target URLs are accessible
3. Check wordlists exist: `ls -la /opt/kraken/wordlists/`

### Telegram Not Sending

1. Verify bot token and chat ID are correct
2. Test bot: Send a message to your bot on Telegram
3. Check logs for errors: `grep -i telegram /opt/kraken/kraken_auto.log`

## Customize Scan Frequency

Edit the timer to change frequency (default: every 2 hours):

```bash
sudo nano /etc/systemd/system/kraken.timer
```

Change `OnUnitActiveSec`:
- `OnUnitActiveSec=30m` - Every 30 minutes
- `OnUnitActiveSec=1h` - Every hour
- `OnUnitActiveSec=2h` - Every 2 hours (default)
- `OnUnitActiveSec=6h` - Every 6 hours

Then reload:

```bash
sudo systemctl daemon-reload
sudo systemctl restart kraken.timer
```

## Wordlists

Default wordlists are in `/opt/kraken/wordlists/`. You can:

1. **Replace defaults**: Overwrite `users.txt` and `passwords.txt`
2. **Add custom lists**: Create new files and reference them in `hidden_services.json`

Example custom wordlists:

```bash
# Download popular wordlists
cd /opt/kraken/wordlists/
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt -O users_common.txt
```

## Security Best Practices

1. **Restrict Access**: Only run as root when necessary
2. **Secure Reports**: Reports contain credentials!
   ```bash
   sudo chmod 700 /opt/kraken/reports/
   ```
3. **Clean Old Reports**: Regularly delete old reports
4. **Use Strong VPS Security**: Enable firewall, use SSH keys
5. **Legal Compliance**: Only scan systems you own or have permission to test

## Next Steps

- Read full documentation: `README_HIDDEN_SERVICES.md`
- Add more targets to `hidden_services.json`
- Customize wordlists for better results
- Setup log rotation for long-term operation
- Monitor Telegram for real-time alerts

## Support

Check logs if something isn't working:
```bash
tail -100 /opt/kraken/kraken_auto.log
sudo journalctl -u kraken.service -n 100
```

## Legal Warning

⚠️ **Use only on systems you own or have explicit permission to test. Unauthorized access is illegal!**

---

*Happy hunting! 🎯*
