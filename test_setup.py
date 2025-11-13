#!/usr/bin/env python3
"""
Test script to validate Kraken hidden service setup
"""

import os
import sys
import json

def test_files_exist():
    """Test that all required files exist"""
    print("Testing file existence...")
    
    required_files = [
        'config.json',
        'hidden_services.json',
        'telegram_reporter.py',
        'kraken_auto.py',
        'files/wordpress_bruteforce_auto.py',
        'files/ssh_bruteforce_auto.py',
        'kraken.service',
        'kraken.timer',
        'install.sh',
        'README_HIDDEN_SERVICES.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            all_exist = False
    
    return all_exist

def test_json_configs():
    """Test that JSON configs are valid"""
    print("\nTesting JSON configurations...")
    
    configs = ['config.json', 'hidden_services.json']
    
    all_valid = True
    for config in configs:
        try:
            with open(config, 'r') as f:
                data = json.load(f)
            print(f"  ✓ {config} - Valid JSON")
        except Exception as e:
            print(f"  ✗ {config} - Invalid: {e}")
            all_valid = False
    
    return all_valid

def test_imports():
    """Test that all modules can be imported"""
    print("\nTesting module imports...")
    
    all_imported = True
    
    try:
        import telegram_reporter
        print("  ✓ telegram_reporter")
    except Exception as e:
        print(f"  ✗ telegram_reporter - {e}")
        all_imported = False
    
    try:
        import kraken_auto
        print("  ✓ kraken_auto")
    except Exception as e:
        print(f"  ✗ kraken_auto - {e}")
        all_imported = False
    
    try:
        from files.wordpress_bruteforce_auto import WordPressBruteForceAuto
        print("  ✓ files.wordpress_bruteforce_auto")
    except Exception as e:
        print(f"  ✗ files.wordpress_bruteforce_auto - {e}")
        all_imported = False
    
    try:
        from files.ssh_bruteforce_auto import SSHBruteForceAuto
        print("  ✓ files.ssh_bruteforce_auto")
    except Exception as e:
        print(f"  ✗ files.ssh_bruteforce_auto - {e}")
        all_imported = False
    
    return all_imported

def test_telegram_reporter():
    """Test Telegram reporter initialization"""
    print("\nTesting Telegram reporter...")
    
    try:
        from telegram_reporter import TelegramReporter
        reporter = TelegramReporter()
        print("  ✓ TelegramReporter initialized")
        print(f"    - Enabled: {reporter.enabled}")
        return True
    except Exception as e:
        print(f"  ✗ TelegramReporter - {e}")
        return False

def test_kraken_auto():
    """Test Kraken auto initialization"""
    print("\nTesting Kraken auto runner...")
    
    try:
        from kraken_auto import KrakenAuto
        runner = KrakenAuto()
        print("  ✓ KrakenAuto initialized")
        print(f"    - Reports dir: {runner.reports_dir}")
        print(f"    - Tor enabled: {runner.config.get('tor', {}).get('enabled', False)}")
        return True
    except Exception as e:
        print(f"  ✗ KrakenAuto - {e}")
        return False

def test_systemd_files():
    """Test systemd service files"""
    print("\nTesting systemd service files...")
    
    all_valid = True
    
    # Check service file
    if os.path.exists('kraken.service'):
        with open('kraken.service', 'r') as f:
            content = f.read()
            if '[Unit]' in content and '[Service]' in content and '[Install]' in content:
                print("  ✓ kraken.service - Valid structure")
            else:
                print("  ✗ kraken.service - Invalid structure")
                all_valid = False
    
    # Check timer file
    if os.path.exists('kraken.timer'):
        with open('kraken.timer', 'r') as f:
            content = f.read()
            if '[Unit]' in content and '[Timer]' in content and '[Install]' in content:
                print("  ✓ kraken.timer - Valid structure")
            else:
                print("  ✗ kraken.timer - Invalid structure")
                all_valid = False
    
    return all_valid

def main():
    """Run all tests"""
    print("="*60)
    print("Kraken Hidden Service Setup - Test Suite")
    print("="*60)
    
    results = []
    
    results.append(("Files exist", test_files_exist()))
    results.append(("JSON configs valid", test_json_configs()))
    results.append(("Module imports", test_imports()))
    results.append(("Telegram reporter", test_telegram_reporter()))
    results.append(("Kraken auto runner", test_kraken_auto()))
    results.append(("Systemd files", test_systemd_files()))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("="*60)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
