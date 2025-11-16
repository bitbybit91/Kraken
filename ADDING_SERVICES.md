# Adding Non-WordPress Services to Kraken

This guide explains how to add different types of services (SSH, FTP, Telnet, etc.) to your `hidden_services.json` configuration file for automated scanning.

## Quick Reference

Currently, Kraken's automated mode supports:
- ✅ **WordPress** - Fully automated
- ✅ **SSH** - Fully automated

Other services from the original Kraken can be added as custom configurations (see below).

## Table of Contents

1. [Adding SSH Services](#adding-ssh-services)
2. [Understanding Service Configuration](#understanding-service-configuration)
3. [Available Service Types](#available-service-types)
4. [Custom Service Integration](#custom-service-integration)
5. [Examples for Different Services](#examples-for-different-services)

---

## Adding SSH Services

SSH is fully supported in automated mode. Here's how to add SSH targets:

### Basic SSH Configuration

```json
{
  "hidden_services": [
    {
      "name": "my_ssh_server",
      "url": "http://example.onion",
      "type": "ssh",
      "port": 22,
      "enabled": true,
      "comment": "SSH server on hidden service",
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    }
  ]
}
```

### SSH on Non-Standard Port

```json
{
  "name": "ssh_custom_port",
  "url": "http://example.onion",
  "type": "ssh",
  "port": 2222,
  "enabled": true,
  "comment": "SSH on custom port 2222",
  "wordlists": {
    "users": "wordlists/ssh_users.txt",
    "passwords": "wordlists/ssh_passwords.txt"
  }
}
```

### SSH on Clearnet (Through Tor)

```json
{
  "name": "clearnet_ssh",
  "url": "http://example.com",
  "type": "ssh",
  "port": 22,
  "enabled": true,
  "comment": "Clearnet SSH server (traffic still goes through Tor)",
  "wordlists": {
    "users": "wordlists/users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

---

## Understanding Service Configuration

Each service entry in `hidden_services.json` has these fields:

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `name` | Yes | Unique identifier for this target | `"target_wordpress"` |
| `url` | Yes | Target URL (http:// or https://) | `"http://example.onion"` |
| `type` | Yes | Service type (wordpress, ssh, etc.) | `"wordpress"` |
| `port` | No | Port number (default depends on service) | `22` |
| `enabled` | No | Enable/disable this target (default: true) | `true` or `false` |
| `comment` | No | Optional note about this target | `"Production server"` |
| `wordlists` | Yes | Username and password lists | See below |

### Wordlists Configuration

```json
"wordlists": {
  "users": "wordlists/users.txt",
  "passwords": "wordlists/passwords.txt"
}
```

You can specify different wordlists for different targets:

```json
"wordlists": {
  "users": "wordlists/admin_users.txt",
  "passwords": "wordlists/weak_passwords.txt"
}
```

---

## Available Service Types

Kraken includes modules for many service types. Currently, only **WordPress** and **SSH** are fully automated.

### Fully Automated (Available Now)

| Service Type | Value | Default Port | Notes |
|--------------|-------|--------------|-------|
| WordPress | `"wordpress"` | 80/443 | Web application brute force |
| SSH | `"ssh"` | 22 | SSH server authentication |

### Original Kraken Modules (Interactive)

These services exist in Kraken but require manual execution:

| Service | Interactive Module | Default Port |
|---------|-------------------|--------------|
| FTP | `ftp_bruteforce.py` | 21 |
| Telnet | `telnet_bruteforce.py` | 23 |
| RDP | `rdp_bruteforce.py` | 3389 |
| CPanel | `cpanel_bruteforce.py` | 2083 |
| Drupal | `drupal_bruteforce.py` | 80/443 |
| Joomla | `joomla_bruteforce.py` | 80/443 |
| Magento | `magento_bruteforce.py` | 80/443 |
| OpenCart | `opencart_bruteforce.py` | 80/443 |
| PrestaShop | `prestashop_bruteforce.py` | 80/443 |
| WooCommerce | `woocommerce_bruteforce.py` | 80/443 |
| Kubernetes | `kubernetes_bruteforce.py` | 6443 |
| LDAP | `ldap_bruteforce.py` | 389 |
| VoIP | `voip_bruteforce.py` | 5060 |
| Office365 | `office365_bruteforce.py` | N/A |
| WiFi | `wifi_bruteforce.py` | N/A |

---

## Custom Service Integration

To add support for other service types (FTP, Telnet, etc.), you need to create automated wrapper modules similar to the existing ones.

### Option 1: Run Existing Modules Manually

You can still use the original Kraken modules interactively:

```bash
cd /opt/kraken
python3 files/ftp_bruteforce.py
# Follow interactive prompts
```

### Option 2: Create Automated Wrapper

To integrate a service into the automated system, create a wrapper module:

1. Copy the pattern from `files/wordpress_bruteforce_auto.py` or `files/ssh_bruteforce_auto.py`
2. Adapt it for your target service
3. Add support in `kraken_auto.py`

**Example structure for FTP:**

```python
# files/ftp_bruteforce_auto.py

import logging
from datetime import datetime

class FTPBruteForceAuto:
    def __init__(self, host, port=21, username_file, password_file, 
                 threads=10, timeout=30, proxies=None):
        self.host = host
        self.port = port
        # ... initialization
    
    def run(self):
        # ... brute force logic
        return self.results
```

Then update `kraken_auto.py`:

```python
def _run_ftp_attack(self, target):
    from files.ftp_bruteforce_auto import FTPBruteForceAuto
    # ... implementation
```

---

## Examples for Different Services

### Multiple WordPress Sites

```json
{
  "hidden_services": [
    {
      "name": "wordpress_blog",
      "url": "http://blog123.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": true,
      "wordlists": {
        "users": "wordlists/wp_users.txt",
        "passwords": "wordlists/wp_passwords.txt"
      }
    },
    {
      "name": "wordpress_shop",
      "url": "http://shop456.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": true,
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/common_passwords.txt"
      }
    }
  ]
}
```

### Multiple SSH Servers

```json
{
  "hidden_services": [
    {
      "name": "ssh_server_1",
      "url": "http://server1.onion",
      "type": "ssh",
      "port": 22,
      "enabled": true,
      "wordlists": {
        "users": "wordlists/linux_users.txt",
        "passwords": "wordlists/ssh_passwords.txt"
      }
    },
    {
      "name": "ssh_server_2",
      "url": "http://server2.onion",
      "type": "ssh",
      "port": 2222,
      "enabled": true,
      "comment": "Custom SSH port",
      "wordlists": {
        "users": "wordlists/admin_users.txt",
        "passwords": "wordlists/weak_passwords.txt"
      }
    }
  ]
}
```

### Mixed Service Types

```json
{
  "hidden_services": [
    {
      "name": "target_wordpress",
      "url": "http://wp.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": true,
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "target_ssh",
      "url": "http://ssh.onion",
      "type": "ssh",
      "port": 22,
      "enabled": true,
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "disabled_target",
      "url": "http://future.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": false,
      "comment": "Will scan later"
    }
  ]
}
```

### Using Different Wordlists

```json
{
  "hidden_services": [
    {
      "name": "target_with_custom_lists",
      "url": "http://example.onion",
      "type": "wordpress",
      "enabled": true,
      "wordlists": {
        "users": "wordlists/custom_usernames.txt",
        "passwords": "wordlists/rockyou_top1000.txt"
      }
    },
    {
      "name": "target_with_default_lists",
      "url": "http://example2.onion",
      "type": "ssh",
      "enabled": true,
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    }
  ]
}
```

---

## Wordlist Management

### Default Wordlists

Located in `/opt/kraken/wordlists/`:
- `users.txt` - Common usernames
- `passwords.txt` - Common passwords

### Creating Custom Wordlists

Create your own wordlists:

```bash
# Create custom username list
cat > /opt/kraken/wordlists/my_users.txt << EOF
admin
administrator
root
user
test
EOF

# Download popular wordlists
cd /opt/kraken/wordlists/
wget https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt -O top1000.txt
```

Then reference them in your config:

```json
"wordlists": {
  "users": "wordlists/my_users.txt",
  "passwords": "wordlists/top1000.txt"
}
```

---

## Enabling/Disabling Targets

### Temporarily Disable a Target

Set `enabled` to `false`:

```json
{
  "name": "temporary_disabled",
  "url": "http://example.onion",
  "type": "wordpress",
  "enabled": false,
  "comment": "Disabled for maintenance"
}
```

### Enable Multiple Targets

Set `enabled` to `true` for each target you want to scan:

```json
{
  "hidden_services": [
    {
      "name": "target1",
      "enabled": true,
      "...": "..."
    },
    {
      "name": "target2",
      "enabled": true,
      "...": "..."
    }
  ]
}
```

---

## Validation

After editing `hidden_services.json`, validate your configuration:

```bash
# Check JSON syntax
python3 -m json.tool /opt/kraken/hidden_services.json

# Test configuration loading
cd /opt/kraken
python3 -c "
import json
with open('hidden_services.json') as f:
    config = json.load(f)
    enabled = [t for t in config.get('hidden_services', []) if t.get('enabled', True)]
    print(f'Found {len(enabled)} enabled target(s)')
    for target in enabled:
        print(f\"  - {target.get('name')} ({target.get('type')}) at {target.get('url')}\")
"
```

---

## Testing

### Test a Single Target

To test a specific configuration without running all targets:

1. Disable all other targets:
```json
{
  "hidden_services": [
    {
      "name": "test_target",
      "enabled": true,
      "...": "..."
    },
    {
      "name": "other_target",
      "enabled": false,
      "...": "..."
    }
  ]
}
```

2. Run manually:
```bash
cd /opt/kraken
sudo python3 kraken_auto.py
```

3. Check results:
```bash
ls -la /opt/kraken/reports/
tail -f /opt/kraken/kraken_auto.log
```

---

## Troubleshooting

### Target Not Being Scanned

**Check 1:** Is `enabled` set to `true`?
```bash
grep -A 10 "my_target_name" /opt/kraken/hidden_services.json | grep enabled
```

**Check 2:** Is the service type supported?
```bash
# Currently only "wordpress" and "ssh" work in automated mode
grep '"type"' /opt/kraken/hidden_services.json
```

**Check 3:** Check logs for errors:
```bash
tail -100 /opt/kraken/kraken_auto.log | grep -i error
```

### Wordlist Not Found

**Error:** `File not found: wordlists/mylist.txt`

**Solution:** Check the path is relative to `/opt/kraken/`:
```bash
ls -la /opt/kraken/wordlists/mylist.txt
```

### Invalid JSON Syntax

**Error:** `json.JSONDecodeError`

**Solution:** Validate JSON syntax:
```bash
python3 -m json.tool /opt/kraken/hidden_services.json
# If valid, it will print formatted JSON
# If invalid, it will show the error
```

---

## Best Practices

### 1. Organize by Service Type

Group services by type for easier management:

```json
{
  "hidden_services": [
    // WordPress sites
    {
      "name": "wp_site1",
      "type": "wordpress",
      "...": "..."
    },
    {
      "name": "wp_site2",
      "type": "wordpress",
      "...": "..."
    },
    // SSH servers
    {
      "name": "ssh_server1",
      "type": "ssh",
      "...": "..."
    },
    {
      "name": "ssh_server2",
      "type": "ssh",
      "...": "..."
    }
  ]
}
```

### 2. Use Descriptive Names

Use clear, descriptive names:
```json
{
  "name": "prod_wordpress_blog",  // Good
  "name": "target1",              // Bad
}
```

### 3. Add Comments

Document your targets:
```json
{
  "name": "main_website",
  "comment": "Main production site - scan weekly",
  "...": "..."
}
```

### 4. Use Appropriate Wordlists

Match wordlists to target type:
- WordPress: Use WordPress-specific username lists (admin, administrator)
- SSH: Use system usernames (root, user, ubuntu)

### 5. Test Before Automating

Always test new targets manually before enabling automated scanning:

```bash
cd /opt/kraken
# Enable only test target
sudo python3 kraken_auto.py
# Check results
# Enable timer only after verification
```

---

## Complete Example Configuration

Here's a complete example showing various service types and configurations:

```json
{
  "hidden_services": [
    {
      "name": "wordpress_blog_onion",
      "url": "http://blogexample123.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": true,
      "comment": "Personal blog on Tor",
      "wordlists": {
        "users": "wordlists/wp_users.txt",
        "passwords": "wordlists/common_passwords.txt"
      }
    },
    {
      "name": "wordpress_shop_clearnet",
      "url": "https://shop.example.com",
      "type": "wordpress",
      "port": 443,
      "enabled": true,
      "comment": "E-commerce site (clearnet through Tor)",
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/rockyou_top1000.txt"
      }
    },
    {
      "name": "ssh_backup_server",
      "url": "http://backup.onion",
      "type": "ssh",
      "port": 22,
      "enabled": true,
      "comment": "Backup server - standard SSH port",
      "wordlists": {
        "users": "wordlists/linux_users.txt",
        "passwords": "wordlists/ssh_passwords.txt"
      }
    },
    {
      "name": "ssh_custom_port",
      "url": "http://server.onion",
      "type": "ssh",
      "port": 2222,
      "enabled": true,
      "comment": "SSH on custom port for security",
      "wordlists": {
        "users": "wordlists/admin_users.txt",
        "passwords": "wordlists/weak_passwords.txt"
      }
    },
    {
      "name": "future_target",
      "url": "http://future.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": false,
      "comment": "Will enable after getting permission"
    }
  ],
  "_comment": "Remember: Only scan systems you own or have permission to test!"
}
```

---

## Next Steps

1. **Edit Configuration:**
   ```bash
   sudo nano /opt/kraken/hidden_services.json
   ```

2. **Validate Syntax:**
   ```bash
   python3 -m json.tool /opt/kraken/hidden_services.json
   ```

3. **Test Manually:**
   ```bash
   cd /opt/kraken
   sudo python3 kraken_auto.py
   ```

4. **Check Results:**
   ```bash
   tail -f /opt/kraken/kraken_auto.log
   ls -la /opt/kraken/reports/
   ```

5. **Enable Automated Scanning:**
   ```bash
   sudo systemctl enable kraken.timer
   sudo systemctl start kraken.timer
   ```

---

## Support

For more information:
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation:** [README_HIDDEN_SERVICES.md](README_HIDDEN_SERVICES.md)
- **Security Guide:** [SECURITY.md](SECURITY.md)

---

## Legal Warning

⚠️ **IMPORTANT:** Only scan systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal.

---

**Last Updated:** 2023-11-16
