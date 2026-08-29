# Security Controls Mapping (NIST CSF 2.0 Alignment)

## Overview
This document maps identified risks from Day 2 to target security controls using the **NIST Cybersecurity Framework (CSF) 2.0** high-level functions: **Govern (GV), Identify (ID), Protect (PR), Detect (DE), Respond (RS), and Recover (RC)**.

## Security Control Mapping Matrix

| Risk | Control | CSF Function | Implementation | Priority | Validation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RISK-01** (Unauthenticated API Access) | API Token Authentication Guard | **Protect (PR.AA)** | Mandatory `Authorization: Bearer <token>` decorator on all `/api/rules` routes in `api.py`. | **P1 (Critical)** | Execute unauthenticated `POST /api/rules` request; verify `401 Unauthorized` status response. |
| **RISK-02** (Rule Injection / Logic Override) | Schema Input Validation Engine | **Protect (PR.DS)** | Enforce strict JSON Schema & Pydantic models on incoming rule payloads before execution. | **P1 (Critical)** | Send malformed JSON payload containing injection string; verify `400 Bad Request` rejection. |
| **RISK-03** (Command Execution in Config) | Safe Subprocess Invocation | **Protect (PR.PS)** | Refactor `config.py` to use argument arrays with `shell=False` to prevent command chaining. | **P2 (High)** | Pass command chaining characters (`&&`, `;`) into config inputs; verify execution safety. |
| **RISK-04** (Outdated Dependency Vulnerability) | Automated Dependency Scanning | **Identify (ID.RA)** | Implement GitHub Dependabot and pin explicit dependency versions in `requirements.txt`. | **P2 (High)** | Run `pip-audit` or `safety check` in local CI/CD sandbox; verify zero known vulnerability flags. |
| **RISK-05** (Log Tampering & Deletion) | Cryptographic Log Chaining | **Detect (DE.CM)** | Implement HMAC-SHA256 hash chaining in `logger.py` with append-only local storage permissions. | **P3 (Medium)** | Attempt manual text modification of `firewall_rules.log`; verify cryptographic hash mismatch alert. |
| **RISK-06** (AI Prompt Injection Context Leak) | Prompt Sandboxing & Filters | **Protect (PR.IR)** | Enforce strict system prompt boundary framing and sanitization on `ai_assist.py` outputs. | **P3 (Medium)** | Submit prompt injection payload (`Ignore previous instructions`); verify systemic boundary response. |
| **RISK-07** (Insecure Plaintext Secrets) | Environment Variable Isolation | **Govern (GV.RM)** | Isolate all sensitive API keys into local `.env` file excluded via `.gitignore`. | **P3 (Medium)** | Execute static secret discovery sweep (`gitleaks`); verify no cleartext secrets in repository code. |
| **RISK-08** (Packet Sniffer Crash / DoS) | Rate-Limiting & Memory Guards | **Respond (RS.AN)** | Implement socket buffer capacity limits and process auto-restart hooks in `packet_sniffer.py`. | **P2 (High)** | Simulate high-volume malformed synthetic packet flood; verify process stability and error handling. |

---

## NIST CSF 2.0 Function Breakdown

* **Govern (GV):** Policy governance, secret storage management, and risk isolation rules.
* **Identify (ID):** Vulnerability identification, supply chain management, and asset scanning.
* **Protect (PR):** Technical access controls, input sanitization, API security, and secure command execution.
* **Detect (DE):** Log integrity checking, continuous monitoring, and anomaly detection.
* **Respond (RS):** System recovery actions, rate-limiting, and error-trapping routines.
* **Recover (RC):** State restoration from backing configuration files following system interruption.
