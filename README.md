#  🔥CyberOS Firewall Engine — Security Assessment & Analyzer

I built this project over a three-week cybersecurity internship at EduRankAI: a working firewall engine, a structured security assessment of that engine, and a small tool that automates part of that assessment.

**Repo:** [https://github.com/rutvikaashtekar1607/Cybersecurity_Intern_-Rutvika-](https://github.com/rutvikaashtekar1607/Cybersecurity_Intern_-Rutvika-)  
**Live docs:** [https://rutvikaashtekar1607.github.io/Cybersecurity_Intern_-Rutvika-/](https://rutvikaashtekar1607.github.io/Cybersecurity_Intern_-Rutvika-/]

## 📝Quick Navigation

- [Week 1: Firewall Foundation](#week-1-firewall-foundation)
- [Week 2: Security Assessment](#week-2-security-assessment)
- [Week 3: Security Analyzer](#week-3-security-analyzer)
- [Repository Structure](#repository-structure)
- [What I'd Flag Myself](#what-id-flag-myself)
- [How to Use This Project](#how-to-use-this-project)

---

## ✅ Week 1: Firewall Foundation

I started by building a core Python firewall engine around a default-DROP policy and real-time threat detection.

### What I implemented:

- **Rule Engine (`rule_engine.py`):** first-match-wins ALLOW/DROP evaluation
- **Packet Sniffer (`packet_sniffer.py`):** Scapy-based Layer 3/4 capture and parsing
- **Connection Tracker (`connection_tracker.py`):** TCP state tracking (SYN → ESTABLISHED → FIN)
- **Alert Engine (`alerts.py`):** port-scan detection (8+ distinct ports in 10s) and volumetric-burst detection (200+ packets in 10s)
- **Logger (`logger.py`):** event logging with a SHA-256 hash field per entry
- **REST API (`api.py`) and CLI (`config.py`):** two ways to manage rules and view alerts
- **AI Assistant (`ai_assist.py`):** heuristic (not ML) risk scoring from alert history

### Test results:

```text
test_rule_engine_default_drop          PASSED ✅
test_rule_engine_allow_match           PASSED ✅
test_connection_tracker_established    PASSED ✅
test_alert_engine_detects_scan         PASSED ✅
test_ai_assist_risk_score_zero         PASSED ✅

5 passed in 0.03s
---

## 🔍 Week 2: Security Assessment

Once the engine worked, I stepped back and reviewed it the way a security analyst would —
reading the code, not scanning it — and produced an asset inventory, a threat model, and a
risk register.

### Asset Inventory (`docs/WEEK2_DAY1_ASSET_INVENTORY.md`)

Asset Inventory (`docs/WEEK2_DAY1_ASSET_INVENTORY.md`)
8 assets, classified by importance:

| Asset | Owner | Importance |
| :--- | :--- | :--- |
| `firewall_rules.json` | Security Admin | Critical |
| Management API (`api.py`) | System Admin | Critical |
| Rule Engine (`rule_engine.py`) | Core Engine | Critical |
| Packet Sniffer (`packet_sniffer.py`) | Core Engine | High |
| Audit Logs (`logger.py`) | Security Ops | High |
| Connection Tracker (`connection_tracker.py`) | Core Engine | High |
| AI Assistant (`ai_assist.py`) | Security Analyst | Medium |
| Alert System (`alerts.py`) | SecOps | Medium |

### Threat Model (`docs/WEEK2_DAY2_THREAT_MODEL.md`)

7 scenarios, mapped to MITRE ATT&CK:

1. Policy bypass via API manipulation — `T1562.008` — Critical
2. Alert suppression via code modification — `T1562.012` — Critical
3. Unauthenticated API access — `T1078.003` — Critical
4. Evidence destruction (alerts lost on restart) — `T1070.001` — Critical
5. Configuration file tampering — `T1027` — Critical
6. Log tampering — `T1070.008` — High
7. Alert fatigue via flooding — `T1498` — High

### Risk Register (`docs/WEEK2_DAY3_RISK_REGISTER.md`)

16 risks — 5 Critical, 5 High, 5 Medium, 1 Low. The five critical ones:

| Risk | Issue | Fix effort |
|---|---|---|
| RISK-001 | No input validation on API | 3 hrs |
| RISK-002 | Alert thresholds hardcoded, can be disabled | 4 hrs |
| RISK-003 | REST API has no authentication | 6 hrs |
| RISK-004 | Alerts stored in-memory only, lost on restart | 8 hrs |
| RISK-005 | Config file has no integrity checks | 5 hrs |

~26 hours estimated to close the critical items.

> These findings came from reading the Week 1 code against a checklist, not from running a
> scanner or penetration test against it. I'd treat them as a strong starting point for
> Week 3 verification rather than an independently audited list.

---

## 🎯 Week 3: Security Analyzer

To act on the Week 2 review, I built a small tool that automates part of it: it reads a
firewall rule set and flags the kinds of issues I was checking for by hand.

** What I implemented:**
- **Rule Parser** (`src/rule_parser.py`) — parses and validates firewall rule JSON
- **Risk Analyzer** (`src/risk_analyzer.py`) — flags overly permissive rules (`0.0.0.0/0`)
  and exposed sensitive ports (Telnet 23, MySQL 3306, etc.)
- **Posture Scorer** (`src/scorer.py`) — turns findings into a numerical risk score
- **Pipeline** (`scripts/run_pipeline.py`) — runs the above end-to-end, writes
  `results/scan_results.json`

**Test results** (Windows / PowerShell, Python 3.14.7, pytest 7.4.0):
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

Combined with Week 1's 5, that's **24 passing tests** across the project.

---

## Repository Structure

```
Cybersecurity_Intern_-Rutvika-/
├── firewall.py, rule_engine.py, alerts.py, logger.py,      Week 1 — root level
│   api.py, config.py, ai_assist.py, connection_tracker.py,
│   packet_sniffer.py, firewall_rules.json
├── tests/test_engine.py                                     Week 1 tests (5)
├── docs/WEEK2_*.md                                           Week 2 assessment
├── 03_Week3_Project/
│   ├── src/rule_parser.py, risk_analyzer.py, scorer.py
│   ├── scripts/run_pipeline.py
│   ├── results/scan_results.json
│   └── tests/test_analyzer.py                                Week 3 tests (19)
├── PRODUCT_MEMO.md
└── requirements.txt
```
## 🤔💭 What I'd Flag Myself

If I were reviewing this project as an outsider, a few things I'd want fixed before calling it production-ready:

- **In-memory state:** connection tracking and alert history (handled by `alerts.py` and `connection_tracker.py` at the root) don't persist across a restart. Fine for a prototype, not for anything that needs forensic history.
- **No API authentication:** the management API (`api.py` at the root) doesn't enforce any auth on its endpoints yet. This is the highest-priority item in the Week 2 risk register (`docs/WEEK2_DAY3_RISK_REGISTER.md`) for a reason.
- **No measured performance numbers:** I haven't benchmarked throughput or CPU overhead for the Week 1 engine (`firewall.py`), so I'm not claiming any here.
- **Week 2 findings are review-based, not scan-based:** the issues noted in `docs/WEEK2_DAY2_THREAT_MODEL.md` are worth actually testing (e.g., hit the API with a bad payload and see what happens) rather than treating the written findings as already-confirmed.

## 🚀 How to Use This Project

```bash
git clone https://github.com/rutvikaashtekar1607/Cybersecurity_Intern_-Rutvika-.git
cd Cybersecurity_Intern_-Rutvika-

# Week 1
pip install -r requirements.txt
pytest tests/ -v
python firewall.py

# Week 3
cd 03_Week3_Project
python -m pytest tests/ -v
python scripts/run_pipeline.py
```

---

## 📞 Contact

- GitHub: [rutvikaashtekar1607](https://github.com/rutvikaashtekar1607)
- LinkedIn: [Rutvika Ashtekar](https://www.linkedin.com/in/rutvikaashtekar07/)
- Email: rutvikaashtekar071604@gmail.com

## 📝 License

MIT — educational project.

---

** 👩🏻‍🏫 Rutvika Mahadev Ashtekar** · Cybersecurity Intern, EduRankAI
