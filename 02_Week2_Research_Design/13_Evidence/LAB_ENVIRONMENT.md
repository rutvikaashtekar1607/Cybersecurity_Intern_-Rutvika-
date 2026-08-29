# Test Environment & Simulation Setup

## 1. Environment Details
* **Operating System:** Ubuntu 22.04 LTS / Windows Subsystem for Linux (WSL2)
* **Runtime:** Python 3.12+
* **Testing Tools:** `pytest`, `curl`, `scapy` (packet injection testing)

## 2. Simulation Procedures
* **API Validation:** Scripted HTTP requests via `curl` testing auth controls.
* **Traffic Simulation:** Synthetic TCP/UDP packet transmission to test sniffer resilience.

## Malware Safety & Isolation Policy
> **SAFETY MANDATE:** Any malware experimentation or dynamic payload testing must use isolated, authorized laboratory environments (e.g., host-only virtual machines, isolated containers, or air-gapped sandboxes). Execution of potentially malicious network traffic or scripts outside strictly authorized local test environments is strictly prohibited.
