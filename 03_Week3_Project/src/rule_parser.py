import json
import sys

def parse_firewall_rules(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        rules = data.get("rules", [])
        print(f"[+] Successfully loaded {len(rules)} rules from {file_path}")
        return rules
    except Exception as e:
        print(f"[-] Error parsing rules: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parse_firewall_rules("../sample_data/firewall_rules.json")