#!/bin/bash
#
# Kraken Installation Script for Ubuntu VPS
# Installs Kraken as a systemd service with Tor support
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║      Kraken Hidden Service Scanner - Installer       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root${NC}"
   exit 1
fi

echo -e "${YELLOW}[*] Installing system dependencies...${NC}"

# Update package list
apt-get update

# Install required packages
apt-get install -y python3 python3-pip tor git

echo -e "${GREEN}[+] System dependencies installed${NC}"

# Install Python dependencies
echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt
pip3 install PySocks  # For SOCKS proxy support

echo -e "${GREEN}[+] Python dependencies installed${NC}"

# Setup Tor
echo -e "${YELLOW}[*] Configuring Tor...${NC}"

# Ensure Tor is configured for SOCKS proxy
if ! grep -q "SOCKSPort 9050" /etc/tor/torrc; then
    echo "SOCKSPort 9050" >> /etc/tor/torrc
fi

# Enable and start Tor
systemctl enable tor
systemctl restart tor

echo -e "${GREEN}[+] Tor configured and started${NC}"

# Create installation directory
INSTALL_DIR="/opt/kraken"
echo -e "${YELLOW}[*] Installing Kraken to ${INSTALL_DIR}...${NC}"

# Create directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy files to installation directory
cp -r ./* "$INSTALL_DIR/"

# Create log directory
mkdir -p /var/log/kraken
chmod 755 /var/log/kraken

# Create reports directory
mkdir -p "$INSTALL_DIR/reports"
chmod 755 "$INSTALL_DIR/reports"

echo -e "${GREEN}[+] Kraken installed to ${INSTALL_DIR}${NC}"

# Install systemd service
echo -e "${YELLOW}[*] Installing systemd service...${NC}"

cp kraken.service /etc/systemd/system/
cp kraken.timer /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

echo -e "${GREEN}[+] Systemd service installed${NC}"

# Configuration
echo -e "${YELLOW}[*] Setting up configuration...${NC}"

# Prompt for Telegram configuration
echo ""
read -p "Do you want to enable Telegram notifications? (y/n): " enable_telegram

if [[ "$enable_telegram" == "y" || "$enable_telegram" == "Y" ]]; then
    read -p "Enter Telegram Bot Token: " bot_token
    read -p "Enter Telegram Chat ID: " chat_id
    
    # Update config.json
    python3 -c "
import json
with open('$INSTALL_DIR/config.json', 'r') as f:
    config = json.load(f)
config['telegram']['bot_token'] = '$bot_token'
config['telegram']['chat_id'] = '$chat_id'
config['telegram']['enabled'] = True
with open('$INSTALL_DIR/config.json', 'w') as f:
    json.dump(config, f, indent=2)
"
    echo -e "${GREEN}[+] Telegram notifications enabled${NC}"
else
    echo -e "${YELLOW}[*] Telegram notifications disabled${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Installation Complete!                      ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Edit hidden services configuration:"
echo "   nano $INSTALL_DIR/hidden_services.json"
echo ""
echo "2. Start the Kraken timer (runs every 2 hours):"
echo "   systemctl enable kraken.timer"
echo "   systemctl start kraken.timer"
echo ""
echo "3. Or run Kraken manually:"
echo "   cd $INSTALL_DIR && python3 kraken_auto.py"
echo ""
echo "4. Check status:"
echo "   systemctl status kraken.timer"
echo "   systemctl list-timers kraken.timer"
echo ""
echo "5. View logs:"
echo "   tail -f /var/log/kraken/kraken.log"
echo "   tail -f $INSTALL_DIR/kraken_auto.log"
echo ""
echo "6. Check reports:"
echo "   ls -la $INSTALL_DIR/reports/"
echo ""
echo -e "${GREEN}Happy hunting!${NC}"
