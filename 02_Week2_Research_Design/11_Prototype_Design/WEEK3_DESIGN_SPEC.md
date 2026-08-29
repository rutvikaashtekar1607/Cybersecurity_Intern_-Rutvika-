# Week 3 Tool Prototype Specification

## 1. Overview
Week 3 focuses on developing the **Firewall Security Posture & Policy Risk Analyzer** tool.

## 2. Functional Architecture
* **Input Parser Module:** Reads `firewall_rules.json` and API rule entries.
* **Static Rule Analysis Engine:** Scans active rules against bad practices (e.g., `0.0.0.0/0` ALLOW rules).
* **Risk Scoring Module:** Computes an aggregated security posture score.
* **Remediation Report Generator:** Outputs actionable fix recommendations.
