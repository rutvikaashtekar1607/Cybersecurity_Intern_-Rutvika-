# Asset Inventory & Classification Matrix

## 1. Overview
This inventory identifies, categorizes, and classifies all digital and system assets within the **CyberOS Firewall Engine** architecture. Classification follows standard CIA (Confidentiality, Integrity, Availability) guidelines to establish security controls based on exposure and impact.

---

## 2. Asset Classification Matrix

| Asset | Owner | Data/Sensitivity | Exposure | Importance | Security Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `firewall_rules.json` | Security Admin | High | Internal Storage | Critical | Confidentiality & Integrity |
| Management API (`api.py`) | System Admin | High | Network Exposed | Critical | Authentication, Authorization & Rate Limiting |
| Rule Engine (`rule_engine.py`) | Core Engine | High | In-Line / Processing | Critical | Input Validation & Robust Exception Handling |
| Packet Sniffer (`packet_sniffer.py`) | Core Engine | Medium | Network Interfaces | High | Least Privilege Execution & Resource Limits |
| Audit Logs (`logger.py`) | Security Ops | Medium | Local File System | High | Tamper-Proof Storage & Log Integrity |
| AI Assistant (`ai_assist.py`) | Security Analyst | Medium | API Endpoint | Medium | Input Sanitization & Output Encoding |
| Connection Tracker (`connection_tracker.py`) | Core Engine | Low | System Memory | High | Memory Management & DoS Mitigation |
| Alert System (`alerts.py`) | SecOps | Low | Internal Event Bus | Medium | Reliable Delivery & Alert Rate Limiting |

---

## 3. Asset Sensitivity & Impact Scale

* **Critical (P1):** Compromise leads to full engine takeover, unauthorized policy override, or complete traffic bypass.
* **High (P2):** Compromise leads to localized service disruption, partial rule corruption, or log suppression.
* **Medium (P3):** Compromise leads to limited information disclosure or performance degradation.
* **Low (P4):** Minor operational impact with zero effect on primary firewall enforcement operations.
