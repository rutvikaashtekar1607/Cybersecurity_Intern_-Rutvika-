from collections import Counter

def recommend_rules(recent_logs, top_n=5):
    """Rule recommendation: suggest ALLOW rules for frequent flows."""
    counts = Counter(
        (log.get("source_ip"), log.get("dest_port"), log.get("protocol"))
        for log in recent_logs
    )
    recs = []
    for (src, port, proto), count in counts.most_common(top_n):
        recs.append({
            "suggested_rule": {"action": "ALLOW", "protocol": proto, "port": port},
            "observed_count": count,
            "rationale": f"{count} packets seen from {src} to port {port}/{proto}."
        })
    return recs

def summarize_traffic_anomalies(alerts):
    """Traffic anomaly summaries."""
    if not alerts:
        return "No anomalies detected."
    by_cat = Counter(a["category"] for a in alerts)
    return f"{len(alerts)} anomalies: " + ", ".join(f"{k} ({v})" for k, v in by_cat.items())

def summarize_logs(logs):
    """Log summarization."""
    if not logs:
        return "No log entries."
    actions = Counter(l.get("action") for l in logs)
    return f"{len(logs)} entries. " + ", ".join(f"{k}: {v}" for k, v in actions.items())

def explain_policy(rule):
    """Policy explanation in plain language."""
    action = "allows" if rule["action"] == "ALLOW" else "drops"
    port = rule.get("port", 0)
    port_desc = f"on port {port}" if port else "on any port"
    return (f"Rule #{rule['id']} {action} {rule.get('protocol','any')} traffic "
            f"{port_desc}. ({rule.get('description','')})")

def score_risk(source_ip, alerts):
    """Risk scoring per source IP."""
    relevant = [a for a in alerts if a.get("source_ip") == source_ip]
    if not relevant:
        return {"source_ip": source_ip, "risk_score": 0, "risk_level": "NONE"}
    weight = {"LOW": 5, "MEDIUM": 15, "HIGH": 40, "CRITICAL": 60}
    score = min(100, sum(weight.get(a["severity"], 5) for a in relevant))
    level = "CRITICAL" if score >= 70 else "HIGH" if score >= 40 else "MEDIUM" if score >= 15 else "LOW"
    return {
        "source_ip": source_ip, "risk_score": score, "risk_level": level,
        "rationale": f"{len(relevant)} alert(s) contributed to this score."
    }
