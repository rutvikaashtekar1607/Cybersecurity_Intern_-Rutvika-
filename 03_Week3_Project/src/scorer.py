def calculate_posture_score(findings):
    score = 100
    weights = {"CRITICAL": 30, "HIGH": 20, "MEDIUM": 10, "LOW": 5}
    
    for finding in findings:
        sev = finding.get("severity", "LOW")
        score -= weights.get(sev, 5)
        
    score = max(0, score)
    
    if score >= 80:
        rating = "GOOD"
    elif score >= 50:
        rating = "MODERATE"
    else:
        rating = "POOR"
        
    return {"score": score, "rating": rating}