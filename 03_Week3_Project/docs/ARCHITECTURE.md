# CyberOS Firewall Policy Analyzer - Architecture & Design

## System Pipeline
1. **Input Ingestion (`rule_parser.py`):** Loads and validates firewall rules from structured JSON payloads.
2. **Analysis Engine (`risk_analyzer.py`):** Evaluates each rule against security baselines (checking for wildcard ports, overly permissive protocols, and insecure IPs).
3. **Scoring Module (`scorer.py`):** Computes an overall security posture score (0-100) based on identified vulnerabilities.
4. **Interface (`cli.py`):** Displays formatted risk findings and security recommendations.