def analyze_rules(rules):
    findings = []
    for rule in rules:
        rule_id = rule.get("id")
        port = rule.get("port")
        protocol = rule.get("protocol")
        source = rule.get("source")
        desc = rule.get("description", "")

        # Check for public exposure of sensitive ports (SSH/Telnet)
        if port in [22, 23] and source == "0.0.0.0/0":
            findings.append({
                "rule_id": rule_id,
                "severity": "CRITICAL" if port == 23 else "HIGH",
                "issue": f"High-risk service (Port {port}) exposed globally to {source}",
                "remediation": "Restrict source IP range to trusted management subnets or VPN."
            })
        
        # Check for ANY protocol / wildcard rules
        if protocol == "ANY" or port == 0:
            findings.append({
                "rule_id": rule_id,
                "severity": "CRITICAL",
                "issue": "Overly permissive rule allows ANY traffic",
                "remediation": "Specify explicit protocols and ports instead of wildcards."
            })
            
    return findings

if __name__ == "__main__":
    from rule_parser import parse_firewall_rules
    rules = parse_firewall_rules("../sample_data/firewall_rules.json")
    results = analyze_rules(rules)
    print(f"[+] Analysis complete. Found {len(results)} security findings.")