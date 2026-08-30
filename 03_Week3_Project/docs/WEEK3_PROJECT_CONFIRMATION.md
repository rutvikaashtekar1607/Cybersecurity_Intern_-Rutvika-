# CyberOS Firewall Security Posture Analyzer — Week 3 Project Confirmation

* **Project Title:** CyberOS Firewall Security Posture Analyzer
* **Selected Cybersecurity Domain:** E. Network Security / Security Posture Assessment Tool
* **Problem Statement:** Modern enterprise networks often suffer from misconfigured firewall policies—such as overly permissive ingress rules (`0.0.0.0/0`) and exposed legacy protocols (e.g., Telnet on port 23 or unencrypted databases)—which significantly increase the attack surface and risk of unauthorized compromise.
* **Proposed Solution:** A modular, automated Python-based security posture analysis pipeline that ingests firewall rule configurations in JSON format, evaluates them against established threat rules, calculates an objective risk posture score, and outputs actionable security findings and remediations.
* **Target User:** Network Administrators, Security Engineers, and Compliance Auditors.
* **Primary Security Outcome:** Automated identification and remediation of critical network access misconfigurations, reducing exposure risk and improving overall firewall security posture.
* **Expected Deliverable:** A fully functional command-line analysis pipeline, automated test suite (`pytest`), architectural documentation, security assessment report, and structured JSON scan outputs (`results/scan_results.json`).
* **Authorized Testing Environment:** Local offline development and testing environment running Python 3.14 with synthetic laboratory firewall rulesets.
* **Tools and Technologies:** Python 3, Pytest, JSON, Git/GitHub, PowerShell.
* **Team Members, if applicable:** Individual Project (Rutvika Mahadev Ashtekar)
* **Individual Responsibilities:** Sole developer responsible for architecture design, rule parser implementation, risk analyzer logic, posture scorer, automated test coverage, and pipeline execution.

---

## Architecture & Implementation Overview

* **Rule Parser (`src/rule_parser.py`):** Ingests and parses your firewall configuration JSON.
* **Risk Analyzer (`src/risk_analyzer.py`):** Evaluates rules and flags critical/high risks (like Telnet and MySQL exposures).
* **Posture Scorer (`src/scorer.py`):** Calculates your risk posture rating (HIGH RISK) and score (70/100).
* **Pipeline (`scripts/run_pipeline.py`):** Automates the end-to-end scan and generates results/scan_results.json.
* **Tests (`tests/test_analyzer.py`):** Passes all 24 automated unit tests successfully.
