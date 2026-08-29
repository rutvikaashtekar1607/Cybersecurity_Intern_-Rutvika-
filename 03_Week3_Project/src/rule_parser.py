import json
import sys
import os

def parse_firewall_rules(file_path=None):
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.normpath(os.path.join(current_dir, "../sample_data/firewall_rules.json"))
        
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        rules = data.get("rules", [])
        print(f"[+] Successfully loaded {len(rules)} rules from {file_path}")
        return rules
    except Exception as e:
        print(f"[-] Error parsing firewall rules: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parse_firewall_rules()