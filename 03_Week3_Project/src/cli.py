import sys
import os
from rule_parser import parse_firewall_rules
from risk_analyzer import analyze_rules
from scorer import calculate_posture_score

def main():
    target_file = "../sample_data/firewall_rules.json"
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    print("=== CyberOS Firewall Policy Risk Analyzer ===")
    rules = parse_firewall_rules(target_file)
    findings = analyze_rules(rules)
    posture = calculate_posture_score(findings)
    
    print(f"\n[Security Posture Score]: {posture['score']}/100 ({posture['rating']})")
    print(f"[Total Findings Identified]: {len(findings)}\n")
    
    for idx, f in enumerate(findings, 1):
        print(f"Finding #{idx}:")
        print(f"  - Rule ID   : {f['rule_id']}")
        print(f"  - Severity  : {f['severity']}")
        print(f"  - Issue     : {f['issue']}")
        print(f"  - Action    : {f['remediation']}")
        print("-" * 40)

if __name__ == "__main__":
    main()