"""Static security checks for CyberOS firewall policies."""

from __future__ import annotations

from typing import Any


ANY_VALUES = {
    "any",
    "0.0.0.0/0",
    "::/0",
    "*",
}

SENSITIVE_PORTS = {
    22: "SSH",
    3389: "RDP",
}


def _is_any(value: Any) -> bool:
    return str(value).strip().lower() in ANY_VALUES


def analyze_rules(
    rules: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Analyse enabled ALLOW rules for defined security weaknesses."""

    findings = []

    for rule in rules:

        if not rule.get("enabled", True):
            continue

        if rule.get("action") != "ALLOW":
            continue

        rule_id = rule["id"]
        source = rule.get("source", "any")
        destination = rule.get("destination", "any")
        port = rule.get("port", "any")
        protocol = str(
            rule.get("protocol", "ANY")
        ).upper()

        # F-001: completely unrestricted ALLOW rule
        if (
            _is_any(source)
            and _is_any(destination)
            and port == "any"
        ):
            findings.append(
                _finding(
                    "F-001",
                    rule_id,
                    "HIGH",
                    "Overly permissive ALLOW rule",
                    "The rule allows traffic from any source "
                    "to any destination on any port.",
                    "Restrict source, destination, protocol, "
                    "and port to the minimum required scope.",
                )
            )
            continue

        # F-002: SSH/RDP exposed to any source
        if (
            _is_any(source)
            and isinstance(port, int)
            and port in SENSITIVE_PORTS
        ):
            service = SENSITIVE_PORTS[port]

            findings.append(
                _finding(
                    "F-002",
                    rule_id,
                    "HIGH",
                    f"Internet-wide {service} exposure",
                    f"The rule allows {service} port "
                    f"{port} from any source.",
                    f"Limit port {port} to approved "
                    "management sources or remove the rule "
                    "if it is not required.",
                )
            )

        # F-003: ANY protocol
        if protocol == "ANY":
            findings.append(
                _finding(
                    "F-003",
                    rule_id,
                    "MEDIUM",
                    "Unrestricted protocol selection",
                    "The ALLOW rule applies to any "
                    "supported protocol.",
                    "Specify only the protocol required "
                    "by the service.",
                )
            )

        # F-004: wildcard network + wildcard port
        if (
            _is_any(source)
            and _is_any(destination)
            and isinstance(port, int)
            and port == 0
        ):
            findings.append(
                _finding(
                    "F-004",
                    rule_id,
                    "HIGH",
                    "Wildcard network scope with "
                    "port wildcard",
                    "The rule combines unrestricted "
                    "source/destination scope with "
                    "a wildcard port value.",
                    "Replace wildcard scope with explicit "
                    "network and service boundaries.",
                )
            )

    return findings


def _finding(
    finding_id: str,
    rule_id: int,
    severity: str,
    title: str,
    description: str,
    recommendation: str,
) -> dict[str, Any]:

    return {
        "finding_id": finding_id,
        "rule_id": rule_id,
        "severity": severity,
        "title": title,
        "description": description,
        "recommendation": recommendation,
    }