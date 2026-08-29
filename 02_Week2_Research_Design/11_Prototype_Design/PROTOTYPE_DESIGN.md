# Prototype & Product Architecture Design (Section 20)

## 1. Product Concept & Problem Statement Alignment

The **CyberOS Firewall Engine** transitions the research, threat modeling, and control mappings established in Week 2 into a functional, modular security software suite.

### Target Tool Domains
1. **Network Security:** Real-time packet interception, dynamic rule evaluation, connection tracking, and traffic anomaly alerting.
2. **AI Security:** Prompt injection boundary sanitization, output exfiltration filtering, and AI assistant query evaluation.

---

## 2. Core Functional Modules & Component Architecture

| Module Name | File Location | Functional Role | Applied Security Control |
| :--- | :--- | :--- | :--- |
| **Core Rule Engine** | `src/rule_engine.py` | State-table lookup engine evaluating IP, Port, and Protocol drop rules. | Input schema validation, zero-trust policy decision point (PDP). |
| **Packet Listener** | `src/packet_sniffer.py` | Asynchronous network traffic sniffer parsing packet headers via raw sockets. | Dropped root capabilities post-binding (`CAP_NET_RAW`), memory buffer limits. |
| **Management API** | `src/api.py` | RESTful API gateway handling administrative rule additions and status checks. | Bearer JWT AuthN, RBAC authorization, endpoint rate-limiting (BOLA/BFLA guards). |
| **Audit Logger** | `src/logger.py` | Centralized append-only event logging daemon. | Cryptographic HMAC-SHA256 log hash chaining for anti-tampering. |
| **Anomaly Detector** | `src/alerts.py` | Real-time traffic rate analyzer triggering automated security alerts. | Threshold-based flood detection, automated IP lockout triggers. |
| **AI Assistant** | `src/ai_assist.py` | Natural-language query interface for SecOps policy analysis. | System prompt boundary isolation, regex output redaction filters. |
| **Configuration Engine** | `src/config.py` | Runtime secret and environment configuration loader. | Zero cleartext hardcoding, explicit `.env` variable ingestion. |

---

## 3. High-Level Modular Data Flow Architecture

```mermaid
graph TD
    %% External Inputs
    NetTraffic[Inbound Packets] -->|1. Capture Headers| Sniffer[Packet Listener - packet_sniffer.py]
    AdminUser[SecOps Admin] -->|2. HTTP Request| API[REST Gateway - api.py]
    
    %% API Control Path
    subgraph Control_Plane [Control Plane - Management]
        API --> AuthGuard{JWT & RBAC Check}
        AuthGuard -- Denied --> Resp401[401/403 Error]
        AuthGuard -- Approved --> SchemaVal[Pydantic Schema Validator]
        SchemaVal --> StateWriter[Update Policy State]
    end

    StateWriter -->|3. Persist State| PolicyDB[(firewall_rules.json)]
    
    %% Packet Processing Path
    subgraph Data_Plane [Data Plane - Packet Processing]
        Sniffer --> FastLookup{Rule Engine Evaluation}
        PolicyDB -.->|Loads Active Rules| FastLookup
        FastLookup -- DROP --> DropAction[Drop Packet & Alert]
        FastLookup -- ALLOW --> PassAction[Forward Packet]
    end

    DropAction --> AlertEngine[Alert Engine - alerts.py]
    FastLookup --> Logger[HMAC Audit Logger - logger.py]
    Logger --> IntegrityLog[(firewall_rules.log)]
