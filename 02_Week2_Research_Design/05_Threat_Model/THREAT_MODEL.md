# Formal Threat Model & Attack Path Analysis

## Rules of Engagement & Testing Boundaries
> **NOTICE:** Threat modeling and attack path mapping are theoretical and for analysis purposes only. No unauthorized exploitation or scanning was attempted against non-authorized systems. All security evaluations are restricted to local lab environments (`127.0.0.1`).

## 1. Threat Actor Profiling

| Actor Category | Description & Capabilities | Motivation | Target Asset | Likelihood |
| :--- | :--- | :--- | :--- | :--- |
| **Opportunistic Attacker** | Scans public ranges for exposed APIs or weak default configurations. | Low-effort compromise, resource hijacking | Management API (`api.py`) | High |
| **Automated Attacker / Bot** | Automated scripts executing brute-force or injection payloads. | Denial of Service, exploitation | API / Packet Listener | High |
| **Insider Threat** | User with valid low-privilege access attempting privilege escalation. | Fraud, data manipulation, control override | Dynamic Rules (`firewall_rules.json`) | Medium |
| **Supply-Chain Attacker** | Compromises upstream Python packages (`scapy`, `flask`). | System takeover, persistent backdoor | Core Engine Environment | Low |
| **Nation-State Actor** | Advanced persistent threat (APT) with zero-day capabilities. | High-value intelligence, covert interception | Active Filtering Logic | Low (Theoretical) |

## 2. Attack Goals Analysis

* **Unauthorized Access:** Gaining unauthenticated access to the management REST API (`api.py`).
* **Data Manipulation:** Tampering with active rules in `firewall_rules.json` to allow malicious traffic.
* **Service Disruption:** Launching DoS/ReDoS attacks against `packet_sniffer.py` to drop network monitoring.
* **Privilege Escalation:** Elevating API user credentials to master admin status.
* **Credential Theft:** Intercepting authorization tokens or API keys passed over unencrypted channels.

## 3. Attack Path Mapping (STRIDE Flow)

Each attack path maps the complete lifecycle from entry to ultimate business impact:

### Path 1: Unauthorized Rule Override (API Injection)
$$\text{Entry Point} \longrightarrow \text{Vulnerability} \longrightarrow \text{Exploitation} \longrightarrow \text{Privilege} \longrightarrow \text{Asset} \longrightarrow \text{Impact}$$

1. **Entry Point:** Management API endpoint `/api/rules`.
2. **Vulnerability:** Unauthenticated or weakly authenticated REST route (OWASP A01).
3. **Exploitation:** Malicious POST request containing custom drop/allow rule parameters.
4. **Privilege:** Administrative policy write execution.
5. **Asset:** Policy storage (`firewall_rules.json`).
6. **Impact:** **Data Manipulation / Unauthorized Access** (Firewall state compromised, malicious traffic permitted).

### Path 2: AI Assistant Context Hijacking (Prompt Injection)
$$\text{Entry Point} \longrightarrow \text{Vulnerability} \longrightarrow \text{Exploitation} \longrightarrow \text{Privilege} \longrightarrow \text{Asset} \longrightarrow \text{Impact}$$

1. **Entry Point:** Natural language query interface (`ai_assist.py`).
2. **Vulnerability:** Lack of input sanitization and prompt boundary enforcement.
3. **Exploitation:** Indirect prompt injection payload passed via security prompt.
4. **Privilege:** Security Analyst read context.
5. **Asset:** AI Assistant internal engine context & memory.
6. **Impact:** **Credential Theft / Information Disclosure** (Exposition of active rules and internal network parameters).

### Path 3: Packet Engine Denial of Service (Sniffer Crash)
$$\text{Entry Point} \longrightarrow \text{Vulnerability} \longrightarrow \text{Exploitation} \longrightarrow \text{Privilege} \longrightarrow \text{Asset} \longrightarrow \text{Impact}$$

1. **Entry Point:** Socket Listener interface (`packet_sniffer.py`).
2. **Vulnerability:** Unhandled malformed packet parsing exception.
3. **Exploitation:** Flood of malformed synthetic TCP packets sent to monitored interfaces.
4. **Privilege:** Network traffic processing thread.
5. **Asset:** Core Rule Engine (`rule_engine.py`).
6. **Impact:** **Service Disruption** (Sniffer process crashes, resulting in unmonitored network traffic).

---

## 4. Threat Modeling Methodology Selection & Rationale

* **Primary Methodology Selected:** **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) combined with **MITRE ATT&CK** tactic mapping.
* **Selection Rationale:**
  1. **Comprehensive Component Coverage:** STRIDE maps directly to software endpoints, data flows, and storage assets identified in Day 1 (`03_Data_Flow`), making it ideal for evaluating application-level security, APIs (`api.py`), and storage files (`firewall_rules.json`).
  2. **Actionable Risk Mitigation:** Categorizing vulnerabilities under STRIDE directly informs engineering controls (e.g., authentication for Spoofing, cryptographic hashes for Tampering, rate-limiting for Denial of Service).
  3. **Standard Alignment:** Integrating MITRE ATT&CK tactic IDs provides industry-standard threat terminology, ensuring seamless risk communication for Week 2 and Week 3 deliverables.
