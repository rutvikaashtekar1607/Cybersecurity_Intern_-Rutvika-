# Data Flow Diagram & Trust Boundaries

## Overview
This document outlines the system boundaries, data flow paths, and trust zones across the CyberOS Firewall Engine and its posture assessment interfaces.

## Data Flow Diagram (Mermaid)

```mermaid
graph TD
    %% Trust Zones
    subgraph External_Untrusted [Untrusted Zone - External Network / Users]
        User[Security Admin / External Request]
        Attacker[Potential Threat Actor]
    end

    subgraph Management_Boundary [Management Trust Boundary]
        API[REST API - api.py]
        AI[AI Assistant Interface - ai_assist.py]
    end

    subgraph Core_Engine_Boundary [Core System Trust Boundary]
        Engine[Packet Rule Engine - rule_engine.py]
        Sniffer[Packet Sniffer - packet_sniffer.py]
        Tracker[Connection Tracker - connection_tracker.py]
    end

    subgraph Data_Storage [Secure Storage Boundary]
        RuleDB[(Firewall Rules - firewall_rules.json)]
        Logger[(Audit Logs - logger.py)]
    end

    %% Data Flow Lines
    User -->|1. Admin HTTP Requests| API
    User -->|2. Natural Language Queries| AI
    Attacker -->|3. Malicious Network Traffic| Sniffer

    API -->|4. Read/Write Policy| RuleDB
    AI -->|5. Read Context / Query| RuleDB
    
    Sniffer -->|6. Raw Network Packets| Engine
    Engine -->|7. State Lookup| Tracker
    Engine -->|8. Evaluate Policy| RuleDB
    Engine -->|9. Security Events & Drops| Logger
    API -->|10. Audit Log Events| Logger
