# Day 5 — Security Test Environment Specification (Section 25)

## 1. Authorized Testing Boundaries & Architecture
To ensure complete compliance with legal, ethical, and organizational safety guidelines, all testing, fuzzing, vulnerability scanning, and threat simulations for the **CyberOS Firewall Engine** will occur strictly within an isolated, authorized local sandbox environment.

### Approved Test Environments
1. **Local Development Machine:** A sandboxed host loopback interface (`127.0.0.1` / `localhost`) running inside user-space Python execution runtimes.
2. **Docker Container Lab:** Ephemeral containerized instances (`alpine:3.19` and python-slim images) running on local Docker engines with restricted bridge networks (`--network bridge-internal`).
3. **Purpose-Built Test Applications:** Local mock servers and synthetic test scripts (`pytest` fixtures) designed specifically to evaluate firewall rule drops and API endpoints.

---

## 2. Environment Infrastructure Specifications

| Parameter | Specification Details |
| :--- | :--- |
| **Hypervisor / Runtime** | Docker Engine v24.0+ / Python 3.11 Virtual Environment (`venv`) |
| **Network Range** | Isolated local loopback (`127.0.0.0/8`) and private Docker subnet (`172.20.0.0/16`) |
| **Target Host OS** | Linux (Ubuntu/Alpine container layers) |
| **Access Control** | Restricted local user execution; root capabilities dropped (`CAP_NET_RAW` isolated via container profiles) |

---

## 3. Strict Prohibited Scope & Out-of-Bounds Restrictions
In strict adherence to ethical security testing protocols, **zero security scanning, packet injection, or penetration testing** shall ever be executed against the following unauthorized assets:
* Public websites and external internet applications.
* Third-party vendor infrastructure or cloud hosting resources.
* University networks, administrative portals, or learning management systems (e.g., Yashwantrao Chavan Maharashtra Open University / Vishwakarma University portals).
* Government systems, municipal networks, or critical infrastructure nodes.
* Corporate infrastructure or personal mobile/desktop devices.
* Any cloud resources (AWS/Azure/GCP) lacking explicit, written authorization and signed scope engagement letters.
