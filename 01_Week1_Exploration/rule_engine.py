# rule_engine.py - Rule Matching Engine

from config import load_rules, save_rules

class RuleEngine:
    def __init__(self):
        self.rules = load_rules()["rules"]
    
    def evaluate_packet(self, packet_info):
        protocol = packet_info.get("protocol", "")
        dest_port = packet_info.get("dest_port", 0)
        
        for rule in self.rules:
            if self._rule_matches(rule, protocol, dest_port):
                return (rule["action"], rule["id"], rule["description"])
        
        return ("DROP", 0, "No matching rule")
    
    def _rule_matches(self, rule, protocol, port):
        rule_protocol = rule.get("protocol", "")
        rule_port = rule.get("port", 0)
        
        if rule_protocol and rule_protocol != protocol:
            return False
        if rule_port != 0 and rule_port != port:
            return False
        return True
    
    def add_rule(self, action, protocol, port, description):
        new_rule = {
            "id": len(self.rules) + 1,
            "action": action,
            "protocol": protocol,
            "port": port,
            "description": description
        }
        self.rules.append(new_rule)
        self._save_rules()
        return new_rule
    
    def delete_rule(self, rule_id):
        self.rules = [r for r in self.rules if r["id"] != rule_id]
        self._save_rules()
        return True
    
    def list_rules(self):
        return self.rules
    
    def _save_rules(self):
        save_rules({"rules": self.rules})

rule_engine = RuleEngine()
