import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rule_engine import RuleEngine
from connection_tracker import ConnectionTracker
from alerts import AlertEngine
import ai_assist


def test_rule_engine_default_drop():
    engine = RuleEngine()
    action, rule_id, desc = engine.evaluate_packet({"protocol": "TCP", "dest_port": 9999})
    assert action == "DROP"

def test_rule_engine_allow_match():
    engine = RuleEngine()
    action, rule_id, desc = engine.evaluate_packet({"protocol": "TCP", "dest_port": 443})
    assert action == "ALLOW"

def test_connection_tracker_established():
    t = ConnectionTracker()
    pkt = {"source_ip": "1.1.1.1", "source_port": 1000, "dest_ip": "2.2.2.2", "dest_port": 443, "protocol": "TCP"}
    t.track(pkt)
    conn = t.track(pkt)
    assert conn["state"] == "ESTABLISHED"

def test_alert_engine_detects_scan():
    a = AlertEngine(scan_port_threshold=5)
    alerts = []
    for port in range(10, 20):
        alerts.extend(a.check({"source_ip": "9.9.9.9", "dest_port": port}))
    assert any(x["category"] == "port_scan" for x in alerts)

def test_ai_assist_risk_score_zero_when_no_alerts():
    result = ai_assist.score_risk("1.1.1.1", [])
    assert result["risk_score"] == 0
