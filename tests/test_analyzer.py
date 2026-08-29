import pytest
import sys
import os

# Add src to path for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from rule_parser import parse_firewall_rules
from risk_analyzer import analyze_rules
from scorer import calculate_posture_score

def test_rule_parser():
    # Construct absolute path to sample data for robust testing
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(base_dir, "../sample_data/firewall_rules.json")
    
    rules = parse_firewall_rules(sample_path)
    assert isinstance(rules, list)
    assert len(rules) > 0

def test_risk_analyzer_findings():
    rules = [
        {"id": 99, "action": "ALLOW", "protocol": "TCP", "port": 23, "source": "0.0.0.0/0", "description": "Telnet"}
    ]
    findings = analyze_rules(rules)
    assert len(findings) == 1
    assert findings[0]["severity"] == "CRITICAL"

def test_scorer_calculation():
    findings = [{"severity": "CRITICAL"}, {"severity": "HIGH"}]
    result = calculate_posture_score(findings)
    assert result["score"] == 50
    assert result["rating"] == "MODERATE"