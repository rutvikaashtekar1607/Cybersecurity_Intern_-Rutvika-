# Comprehensive Risk Register & Risk Assessment Matrix

## 1. Methodology & Risk Scoring Framework

> **Scoring Rationale Note:** Risk ratings in this matrix are derived using qualitative security assessment models. While numerical mappings (1–5) are used for structured prioritization, they represent qualitative risk levels rather than scientifically precise statistical metrics.

### Likelihood Scale Definition
* **1 - Rare:** Highly unlikely to occur; requires complex prerequisites or zero-day conditions.
* **2 - Unlikely:** Could occur under unusual conditions; low actor capability.
* **3 - Possible:** Might occur at some point; standard opportunistic scanning target.
* **4 - Likely:** Expected to occur in most circumstances; automated script targets.
* **5 - Almost Certain:** Continuous exploitation vector; easily discovered exposed surface.

### Impact Scale Definition
* **1 - Negligible:** Minor operational nuisance; zero exposure of sensitive state.
* **2 - Minor:** Localized impact; non-critical component slowdown.
* **3 - Moderate:** Partial function degradation; limited data leakage.
* **4 - Major:** Substantial disruption; unauthorized modification of rule logic.
* **5 - Severe:** Complete firewall engine takeover, bypass of security rules, or total service destruction.

### Qualitative Risk Matrix Calculation Formula

$$\text{Risk Level} = \text{Likelihood Rating} \times \text{Impact Rating}$$

* **Critical (20 – 25):** Immediate emergency remediation required; system unsafe for operation.
* **High (12 – 19):** Urgent priority fix required within initial development sprint.
* **Medium (6 – 11):** Standard priority fix; scheduled for secondary update cycle.
* **Low (1 – 5):** Acceptable operational risk; monitored via standard logging.

## 2. Risk Matrix Table

| Risk ID | Vulnerability / Threat Scenario | Asset | Likelihood | Impact | Calculated Score | Overall Risk Rating | Risk Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RISK-01** | Unauthenticated API Access to Rule Management | Management API (`api.py`) | 4 (Likely) | 5 (Severe) | 20 | **Critical** | Implement mandatory JWT/API key authentication decorators. |
| **RISK-02** | Rule Injection & Logic Override via Schema Bypass | Rule Engine (`rule_engine.py`) | 4 (Likely) | 5 (Severe) | 20 | **Critical** | Enforce Pydantic schema validation prior to rule execution. |
| **RISK-03** | Command Execution via Subprocess Wrappers | Config Engine (`config.py`) | 3 (Possible) | 4 (Major) | 12 | **High** | Replace shell invocation (`shell=True`) with fixed array calls. |
| **RISK-04** | Deprecated Dependency Vulnerability Exposure | Listener (`packet_sniffer.py`) | 4 (Likely) | 3 (Moderate) | 12 | **High** | Pin dependency versions in `requirements.txt` & automate scanning. |
| **RISK-05** | Local Audit Log Tampering / Deletion | Audit Logger (`logger.py`) | 2 (Unlikely) | 3 (Moderate) | 6 | **Medium** | Cryptographic HMAC hash chaining and append-only permissions. |
| **RISK-06** | Context Leakage via AI Prompt Injection | AI Assistant (`ai_assist.py`) | 3 (Possible) | 2 (Minor) | 6 | **Medium** | System prompt boundary isolation and output filtering. |
| **RISK-07** | Insecure Plaintext Storage of Secrets | Environment (`.env`) | 2 (Unlikely) | 4 (Major) | 8 | **Medium** | Enforce `.gitignore` policy and environment key isolation. |

## 3. Risk Mitigation Hierarchy
1. **Immediate Focus:** Address Critical risks (RISK-01, RISK-02) during Day 2 architecture design updates.
2. **Sprint Prioritization:** Remediate High risks (RISK-03, RISK-04) prior to Week 3 functional prototype release.
3. **Continuous Monitoring:** Maintain Medium risks (RISK-05, RISK-06, RISK-07) under standard logging and periodic audit reviews.
