# Master Security Testing Plan (Section 18)

## Rules of Engagement & Test Scope Disclaimer
> **NOTICE:** All testing routines documented in this plan are restricted exclusively to authorized, local synthetic environments (`127.0.0.1`) and containerized labs. No unauthorized scanning or exploitation was performed against third-party systems.

---

## 1. Comprehensive Test Execution Matrix

This test plan defines functional, negative, structural, and operational security verification suites for the **CyberOS Firewall Engine**.

| Test ID | Test Category | Target Component | Scenario & Description | Expected Result | Pass / Fail Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST-01** | **Functional Security** | Core Engine (`rule_engine.py`) | Execute packet matching against active block rule (e.g., DROP IP `192.168.1.50`). | Inbound packet matching rule is dropped instantly. | **Pass:** Traffic dropped; rule match count incremented. |
| **TEST-02** | **Negative Testing** | Management API (`api.py`) | Submit malformed JSON payload and invalid HTTP verbs to `/api/v1/rules`. | System safely rejects payload without crashing or throwing stack trace. | **Pass:** Returns `400 Bad Request` or `405 Method Not Allowed`. |
| **TEST-03** | **Authentication** | Management API (`api.py`) | Send POST request to `/api/v1/rules` without presenting a Bearer JWT header. | Request denied; zero access granted to administrative routes. | **Pass:** Returns `401 Unauthorized`. |
| **TEST-04** | **Authorization** | Management API (`api.py`) | Submit rule modification request using a valid `Operator` (Read-Only) token. | Action blocked due to insufficient privilege claims. | **Pass:** Returns `403 Forbidden`. |
| **TEST-05** | **Input Validation** | Schema Parser (`rule_engine.py`) | Inject OS command characters (`127.0.0.1; cat /etc/passwd`) into IP string field. | Schema validator flags invalid IP syntax and drops input. | **Pass:** Input rejected with validation error; no shell execution. |
| **TEST-06** | **Configuration** | Environment Config (`config.py`) | Scan configuration parameters for weak default API keys or `DEBUG=True` flags. | Secure defaults enforced; debug flags disabled in non-dev state. | **Pass:** Zero default fallback credentials present in active config. |
| **TEST-07** | **Dependency Audit** | Supply Chain (`requirements.txt`) | Execute automated vulnerability scanner (`pip-audit` / `trivy`) against project packages. | Zero High or Critical CVE vulnerabilities identified in third-party libraries. | **Pass:** Clean audit report generated. |
| **TEST-08** | **Logging Tests** | Audit Logger (`logger.py`) | Trigger failed authentication attempt and verify entry in `firewall_rules.log`. | Security event logged with timestamp, source IP, event type, and HMAC hash. | **Pass:** Log entry created and HMAC signature verified. |
| **TEST-09** | **Detection Tests** | Anomaly Alerts (`alerts.py`) | Simulate high-rate brute force login attempts (10 failed attempts within 5 seconds). | System detects pattern anomaly and triggers alert event. | **Pass:** Alert generated and source IP temporarily rate-limited. |

---

## 2. Detailed Category Breakdown

### Functional & Negative Security Testing
* **Objective:** Verify that security controls function as specified under normal conditions and recover gracefully under adversarial conditions.
* **Methodology:** Automated pytest execution against local test fixtures in `tests/`.

### AuthN, AuthZ & Privilege Escalation Testing
* **Objective:** Ensure protected resources cannot be accessed without valid credentials or by roles lacking administrative permission.
* **Methodology:** Token tampering, role swapping, and missing header injection via automated HTTP test client scripts.

### Input Validation & Defensive Resilience Testing
* **Objective:** Guarantee that all inputs (API JSON bodies, CLI flags, network packet headers) are strictly validated before internal evaluation.
* **Methodology:** Fuzzing input fields with boundary-breaking strings, SQL/Command injection patterns, and malformed packet structures.

### Supply Chain, Configuration & Auditing Verification
* **Objective:** Ensure zero static secrets, clean dependency trees, continuous event logging, and active anomaly detection.
* **Methodology:** CI/CD integration with static code analyzers, dependency audit runners, and log hash integrity checkers.
