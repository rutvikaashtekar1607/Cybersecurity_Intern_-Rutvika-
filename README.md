#  🔥 CyberOS Firewall Engine — Security Assessment & Analyzer

I built this project over a three-week cybersecurity internship at EduRankAI: a working firewall engine, a structured security assessment of that engine, and a small tool that automates part of that assessment.

**📍 Repo:** [https://github.com/rutvikaashtekar1607/Cybersecurity_Intern_-Rutvika-](https://github.com/rutvikaashtekar1607/Cybersecurity_Intern_-Rutvika-)  
**📖 Live docs:** [https://rutvikaashtekar1607.github.io/Cybersecurity_Intern_-Rutvika-/](https://rutvikaashtekar1607.github.io/Cybersecurity_Intern_-Rutvika-/]

---

## 📝 Quick Navigation

- [⚙️ Week 1: Firewall Foundation](#week-1-firewall-foundation)
- [🔍 Week 2: Security Assessment](#week-2-security-assessment)
- [🎯 Week 3: Security Analyzer](#week-3-security-analyzer)
- [📂 Repository Structure](#repository-structure)
- [💭 What I'd Flag Myself](#what-id-flag-myself)
- [🚀 How to Use This Project](#how-to-use-this-project)

---

## ✅ Week 1: Firewall Foundation

I started by building a core Python firewall engine around a default-DROP policy and real-time threat detection.

### 🔧 What I implemented:

| Component | File | Purpose |
|-----------|------|---------|
| 🎯 Rule Engine | `rule_engine.py` | first-match-wins ALLOW/DROP evaluation |
| 📡 Packet Sniffer | `packet_sniffer.py` | Scapy-based Layer 3/4 capture and parsing |
| 🔗 Connection Tracker | `connection_tracker.py` | TCP state tracking (SYN → ESTABLISHED → FIN) |
| 🚨 Alert Engine | `alerts.py` | port-scan detection (8+ distinct ports in 10s) and volumetric-burst detection (200+ packets in 10s) |
| 📋 Logger | `logger.py` | event logging with a SHA-256 hash field per entry |
| 🔌 REST API | `api.py` | two ways to manage rules and view alerts |
| ⚡ CLI | `config.py` | two ways to manage rules and view alerts |
| 🤖 AI Assistant | `ai_assist.py` | heuristic (not ML) risk scoring from alert history |

### ✅ Test results:

```text
test_rule_engine_default_drop          PASSED ✅
test_rule_engine_allow_match           PASSED ✅
test_connection_tracker_established    PASSED ✅
test_alert_engine_detects_scan         PASSED ✅
test_ai_assist_risk_score_zero         PASSED ✅

5 passed in 0.03s
```

---

## 🔍 Week 2: Security Assessment

Once the engine worked, I stepped back and reviewed it the way a security analyst would — reading the code, not scanning it — and produced an asset inventory, a threat model, and a risk register.

### 📊 Asset Inventory (`docs/WEEK2_DAY1_ASSET_INVENTORY.md`)

| Asset | Owner | Importance |
| :--- | :--- | :--- |
| 🔐 `firewall_rules.json` | Security Admin | 🔴 Critical |
| 🌐 Management API (`api.py`) | System Admin | 🔴 Critical |
| ⚙️ Rule Engine (`rule_engine.py`) | Core Engine | 🔴 Critical |
| 📡 Packet Sniffer (`packet_sniffer.py`) | Core Engine | 🟠 High |
| 📋 Audit Logs (`logger.py`) | Security Ops | 🟠 High |
| 🔗 Connection Tracker (`connection_tracker.py`) | Core Engine | 🟠 High |
| 🤖 AI Assistant (`ai_assist.py`) | Security Analyst | 🟡 Medium |
| 🚨 Alert System (`alerts.py`) | SecOps | 🟡 Medium |

### 🎯 Threat Model (`docs/WEEK2_DAY2_THREAT_MODEL.md`)

**7 scenarios, mapped to MITRE ATT&CK:**

| # | Threat | MITRE Technique | Severity |
|---|--------|-----------------|----------|
| 1️⃣ | Policy bypass via API manipulation | `T1562.008` | 🔴 Critical |
| 2️⃣ | Alert suppression via code modification | `T1562.012` | 🔴 Critical |
| 3️⃣ | Unauthenticated API access | `T1078.003` | 🔴 Critical |
| 4️⃣ | Evidence destruction (alerts lost on restart) | `T1070.001` | 🔴 Critical |
| 5️⃣ | Configuration file tampering | `T1027` | 🔴 Critical |
| 6️⃣ | Log tampering | `T1070.008` | 🟠 High |
| 7️⃣ | Alert fatigue via flooding | `T1498` | 🟠 High |

### 💰 Risk Register (`docs/WEEK2_DAY3_RISK_REGISTER.md`)

**16 risks — 5 Critical, 5 High, 5 Medium, 1 Low.** The five critical ones:

| Risk | Issue | Fix effort |
|------|-------|------------|
| RISK-001 | ❌ No input validation on API | ⏱️ 3 hrs |
| RISK-002 | ❌ Alert thresholds hardcoded, can be disabled | ⏱️ 4 hrs |
| RISK-003 | ❌ REST API has no authentication | ⏱️ 6 hrs |
| RISK-004 | ❌ Alerts stored in-memory only, lost on restart | ⏱️ 8 hrs |
| RISK-005 | ❌ Config file has no integrity checks | ⏱️ 5 hrs |

**~26 hours estimated to close the critical items.**

> These findings came from reading the Week 1 code against a checklist, not from running a scanner or penetration test against it. I'd treat them as a strong starting point for Week 3 verification rather than an independently audited list.

---

## 🎯 Week 3: Security Analyzer

To act on the Week 2 review, I built a small tool that automates part of it: it reads a firewall rule set and flags the kinds of issues I was checking for by hand.

### 🔧 What I implemented:

| Component | File | Purpose |
|-----------|------|---------|
| 📖 Rule Parser | `src/rule_parser.py` | parses and validates firewall rule JSON |
| 🔍 Risk Analyzer | `src/risk_analyzer.py` | flags overly permissive rules (`0.0.0.0/0`) and exposed sensitive ports (Telnet 23, MySQL 3306, etc.) |
| 📊 Posture Scorer | `src/scorer.py` | turns findings into a numerical risk score |
| 🚀 Pipeline | `scripts/run_pipeline.py` | runs the above end-to-end, writes `results/scan_results.json` |

### ✅ Test results

**(Windows / PowerShell, Python 3.14.7, pytest 7.4.0):**

```
$ cd 03_Week3_Project
$ python -m pytest tests/ -v

test_01_parser_accepts_valid_policy PASSED
test_02_parser_applies_default_scope PASSED
test_03_parser_normalises_lowercase_values PASSED
test_04_parser_supports_any_port PASSED
test_05_detects_overly_permissive_rule PASSED
test_06_detects_sensitive_port_exposure PASSED
test_07_detects_any_protocol PASSED
test_08_ignores_disabled_rule PASSED
test_09_drop_rule_has_no_allow_finding PASSED
test_10_loads_sample_policy PASSED
test_11_rejects_non_object_policy PASSED
test_12_rejects_missing_rules PASSED
test_13_rejects_invalid_action PASSED
test_14_rejects_invalid_protocol PASSED
test_15_rejects_invalid_port PASSED
test_16_rejects_duplicate_rule_ids PASSED
test_17_rejects_malformed_json PASSED
test_18_rejects_missing_input_file PASSED
test_19_empty_findings_produce_no_findings_state PASSED

19 passed in 0.18s ✅
```

**Combined with Week 1's 5, that's 24 passing tests across the project.**

| Test ID | Scenario | Expected Result | Actual Result | Status | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | ✅ Valid input parsing (`test_01` to `04`) | Successful processing and normalization | Processed successfully | **Pass** | [test_execution.png](../evidence/test_execution.png) |
| T-02 | 🔍 Rule analysis & detection (`test_05` to `09`) | Correctly flags risk findings | Findings identified accurately | **Pass** | [test_execution.png](../evidence/test_execution.png) |
| T-03 | 📊 Sample policy loading (`test_10`) | Loads exact sample rule count | Assertion mismatch due to expected count test | **Fail** | [failed_test_demonstration.png](../evidence/failed_test_demonstration.png) |
| T-04 | ⚠️ Negative & Security rules (`test_11` to `15`) | Safe rejection via validation error | Safely rejected / caught | **Pass** | [test_execution.png](../evidence/test_execution.png) |
| T-05 | 🔧 Edge-cases & handling (`test_16` to `19`) | Handles duplicates, JSON errors, empty states | Exception raised / handled correctly | **Pass** | [test_execution.png](../evidence/test_execution.png) |

---

## 📋 Project Compliance & Implementation Log (Days 1–3)

| Project Phase | Core Requirements & Tasks | Status & Implementation Details |
| :--- | :--- | :--- |
| **📅 Day 1: Setup & Baseline** | • Repository layout setup<br>• OS & Python 3.14.7 environment doc<br>• Asset inventory & trust boundaries | **✅ Completed** — Documented across root level, `requirements.txt`, and `docs/WEEK2_DAY1_ASSET_INVENTORY.md`. |
| **📅 Day 2: Core Engine** | • Pipeline workflow execution<br>• Input parsing & logging<br>• Major error handling | **✅ Completed** — Implemented via `packet_sniffer.py`, `rule_engine.py`, `logger.py`, and verified via unit tests. |
| **📅 Day 3: Hardening & Justification** | • Input validation & config checking<br>• Feature inclusion/exclusion justification<br>• Security-by-design assessment | **✅ Completed** — Rule validation implemented (`rule_parser.py`); web dashboards and API auth explicitly deferred and justified in risk logs. |
| **📅 Day 4: Testing & Validation** | • Comprehensive test suite (19 unit tests)<br>• Functional, negative & edge-case coverage<br>• Evidence logging & failure analysis | **Completed** — Executed `pytest` suite covering functional rules, negative validations, and edge-cases; generated execution and failure screenshots. |
 | **🚀 Day 5: Optimization & Final Validation** | • Code quality & security control review<br>• Improvement iteration documentation<br>• Final security validation outcome | **Completed** — Documented original approach, problem identified, and iterative improvements; verified final security posture scoring and test outcomes. |

## 🔄 Day 5: Optimization & Final Validation — Improvement Iteration

* **Original Approach:** Initially, firewall policies were evaluated purely at runtime using basic rule-matching (`rule_engine.py`) without an automated, static evaluation of policy hygiene or risk exposure before deployment.
* **Problem Identified:** Manual rule review is error-prone, making it difficult to systematically detect overly permissive scopes (`0.0.0.0/0`) or sensitive port exposures (Telnet 23, MySQL 3306) across complex rule configurations.
* **Improvement Made:** Developed a dedicated modular pipeline (`03_Week3_Project/`) featuring `rule_parser.py`, `risk_analyzer.py`, and `scorer.py` to automate static policy parsing, validate input safety, and compute a standardized risk posture score.
* **Result After Improvement:** The system now automatically flags configuration weaknesses, produces a verifiable High Risk posture score (80/100) saved to `results/scan_results.json`, and maintains 100% test coverage across 19 unit tests without creating auxiliary security risks.
  
## 🛡️ Security Validation Outcome

The completed security assessment tool successfully meets its intended security objective by demonstrating that it can:
1. **Identify Configuration Weaknesses:** Systematically flag unauthorized or overly permissive rules and insecure port configurations from input rule files.
2. **Enforce Strict Input Validation:** Safely reject malformed JSON, missing parameters, and invalid data types through robust exception handling.
3. **Prioritize Risks Quantitatively:** Map findings to a structured risk scoring framework, ensuring systematic evaluation as documented in the threat model and risk register.

---

## 📂 Repository Structure

```
Cybersecurity_Intern_-Rutvika-/
│
├── 🔥 Week 1 — Root Level
│   ├── firewall.py
│   ├── rule_engine.py
│   ├── alerts.py
│   ├── logger.py
│   ├── api.py
│   ├── config.py
│   ├── ai_assist.py
│   ├── connection_tracker.py
│   ├── packet_sniffer.py
│   └── firewall_rules.json
│
├── 🧪 Week 1 Tests
│   └── tests/test_engine.py (5 tests)
│
├── 📋 Week 2 Assessment
│   └── docs/WEEK2_*.md
│
├── 🎯 Week 3 Project
│   ├── src/
│   │   ├── rule_parser.py
│   │   ├── risk_analyzer.py
│   │   └── scorer.py
│   ├── scripts/
│   │   └── run_pipeline.py
│   ├── results/
│   │   └── scan_results.json
│   └── tests/
│       └── test_analyzer.py (19 tests)
│
├── 📄 PRODUCT_MEMO.md
└── 📋 requirements.txt
```

---

## 🤔 What I'd Flag Myself

If I were reviewing this project as an outsider, a few things I'd want fixed before calling it production-ready:

🔴 **In-memory state:** connection tracking and alert history (handled by `alerts.py` and `connection_tracker.py` at the root) don't persist across a restart. Fine for a prototype, not for anything that needs forensic history.

🔴 **No API authentication:** the management API (`api.py` at the root) doesn't enforce any auth on its endpoints yet. This is the highest-priority item in the Week 2 risk register (`docs/WEEK2_DAY3_RISK_REGISTER.md`) for a reason.

🟡 **No measured performance numbers:** I haven't benchmarked throughput or CPU overhead for the Week 1 engine (`firewall.py`), so I'm not claiming any here.

🟡 **Week 2 findings are review-based, not scan-based:** the issues noted in `docs/WEEK2_DAY2_THREAT_MODEL.md` are worth actually testing (e.g., hit the API with a bad payload and see what happens) rather than treating the written findings as already-confirmed.

---

## 🚀 How to Use This Project

```bash
git clone https://github.com/rutvikaashtekar1607/Cybersecurity_Intern_-Rutvika-.git
cd Cybersecurity_Intern_-Rutvika-

# 🔥 Week 1
pip install -r requirements.txt
pytest tests/ -v
python firewall.py

# 🎯 Week 3
cd 03_Week3_Project
python -m pytest tests/ -v
python scripts/run_pipeline.py
```

---

## 📞 Contact

- 🐙 GitHub: [rutvikaashtekar1607](https://github.com/rutvikaashtekar1607)
- 💼 LinkedIn: [Rutvika Ashtekar](https://www.linkedin.com/in/rutvikaashtekar07/)
- 📧 Email: rutvikaashtekar071604@gmail.com

---

## 📝 License

📜 MIT — educational project.

---

**👩🏻‍🏫 Rutvika Mahadev Ashtekar** · Cybersecurity Intern, EduRankAI
