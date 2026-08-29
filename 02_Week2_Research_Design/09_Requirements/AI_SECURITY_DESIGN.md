# AI & LLM Security Design & Guardrails (Section 17)

## 1. LLM Threat Landscape & Security Matrix

This document evaluates the AI security posture of the internal security assistant (`ai_assist.py`) using the **OWASP Top 10 for LLM Applications** framework.

| Vulnerability Vector | Risk Scenario in CyberOS | Applied Guardrail & Mitigation | Enforcement Mechanism |
| :--- | :--- | :--- | :--- |
| **Prompt Injection** | Attacker injects system prompts via rule comments to override safety guardrails. | Strict input sanitization, delimiter isolation (`<user_input>`), and system prompt locking. | `ai_assist.py` Pre-Filter |
| **Sensitive Data Leakage** | Assistant reveals internal API keys, raw environment variables, or private hash strings. | Regex-based data redaction filter executing on model output stream prior to response rendering. | Output Sanitizer |
| **Excessive Agency** | AI Assistant attempting direct command execution or autonomous policy deletion. | Read-Only execution context. Model outputs structural suggestions only, zero direct file write access. | Architectural RBAC |
| **Unsafe Tool Use** | AI invoking local OS sub-shells or untrusted python interpreter commands. | Strict function calling allowlist using typed JSON schemas; shell invocations explicitly banned. | Tool Execution Guard |
| **Retrieval Poisoning** | Adversary inserting malicious rule logic into training/RAG context datasets. | Hash-verified local documentation stores with cryptographic integrity checks prior to model loading. | Document HMAC Checker |
| **Insecure Output Handling** | AI output rendering raw JavaScript or HTML strings resulting in XSS in SecOps dashboard. | Markdown-only text rendering with complete HTML/script tag stripping. | Presentation Layer Filter |
| **Model Supply Chain** | Compromised upstream HuggingFace model weights or library dependencies. | Hash verification of local GGUF/PyTorch model weights and strict dependency version pinning. | SHA-256 Checksums |
| **AuthN & AuthZ** | Unauthenticated user querying security assistant for network architecture data. | Mandatory JWT token evaluation prior to passing user prompt to the AI processing thread. | `api.py` Middleware |

---

## 2. Guardrail Execution Architecture

```mermaid
graph TD
    UserQuery[User Security Query] --> AuthCheck{JWT Auth Guard}
    AuthCheck -- Unauthorized --> Reject[401 Unauthorized]
    AuthCheck -- Authorized --> PromptSanitizer[Input Sanitizer & Boundary Wrappers]
    
    PromptSanitizer -->|Clean Prompt| LLMEngine[LLM Engine / ai_assist.py]
    LLMEngine --> RawOutput[Raw Model Response]
    
    RawOutput --> RedactionFilter[Output Redaction Filter - Mask Secrets/Keys]
    RedactionFilter --> OutputEncoder[HTML/Entity Encoder]
    OutputEncoder --> SafeResponse[Final User Response]
