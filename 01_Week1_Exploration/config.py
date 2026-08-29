# config.py - Firewall Configuration

import json
import os

CONFIG_FILE = "firewall_config.json"
LOG_FILE = "firewall.log"
RULES_FILE = "firewall_rules.json"

DEFAULT_RULES = {
    "rules": [
        {"id": 1, "action": "ALLOW", "protocol": "TCP", "port": 22, "description": "SSH"},
        {"id": 2, "action": "ALLOW", "protocol": "TCP", "port": 80, "description": "HTTP"},
        {"id": 3, "action": "ALLOW", "protocol": "TCP", "port": 443, "description": "HTTPS"},
        {"id": 4, "action": "DROP", "protocol": "TCP", "port": 0, "description": "Default DROP"}
    ]
}

def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, 'r') as f:
            return json.load(f)
    else:
        save_rules(DEFAULT_RULES)
        return DEFAULT_RULES

def save_rules(rules):
    with open(RULES_FILE, 'w') as f:
        json.dump(rules, f, indent=2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
        import shutil
import time

BACKUP_DIR = "backups"

def backup_config():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        save_config({})
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"config-{stamp}.json")
    shutil.copy2(CONFIG_FILE, backup_path)
    return backup_path

def list_backups():
    if not os.path.isdir(BACKUP_DIR):
        return []
    return sorted(f for f in os.listdir(BACKUP_DIR) if f.startswith("config-"))

def restore_config(backup_filename):
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    shutil.copy2(backup_path, CONFIG_FILE)
    return load_config()
