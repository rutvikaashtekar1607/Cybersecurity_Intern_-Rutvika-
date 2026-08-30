"""Validation and loading for CyberOS firewall policy files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RuleValidationError(ValueError):
    """Raised when a firewall policy is not in the expected format."""


def _normalise_port(value: Any, rule_number: int) -> int | str:
    if value in (None, "", "any", "ANY"):
        return "any"

    if isinstance(value, bool):
        raise RuleValidationError(
            f"Rule {rule_number}: port must be an integer or 'any'."
        )

    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise RuleValidationError(
            f"Rule {rule_number}: port must be an integer or 'any'."
        ) from exc

    if not 0 <= port <= 65535:
        raise RuleValidationError(
            f"Rule {rule_number}: port must be between 0 and 65535."
        )

    return port


def validate_policy(data: Any) -> list[dict[str, Any]]:
    """Validate and normalise a firewall policy.

    Expected format:

        {
            "rules": [...]
        }

    Source and destination are optional for compatibility with the
    Week 1 firewall rule format.
    """

    if not isinstance(data, dict):
        raise RuleValidationError(
            "Policy must be a JSON object containing 'rules'."
        )

    rules = data.get("rules")

    if not isinstance(rules, list):
        raise RuleValidationError(
            "Policy must contain a 'rules' list."
        )

    if not rules:
        raise RuleValidationError(
            "Policy must contain at least one rule."
        )

    normalised = []
    seen_ids = set()

    for position, raw_rule in enumerate(rules, start=1):

        if not isinstance(raw_rule, dict):
            raise RuleValidationError(
                f"Rule {position}: each rule must be an object."
            )

        rule_id = raw_rule.get("id", position)

        if isinstance(rule_id, bool) or not isinstance(rule_id, int):
            raise RuleValidationError(
                f"Rule {position}: id must be an integer."
            )

        if rule_id in seen_ids:
            raise RuleValidationError(
                f"Rule {position}: duplicate rule id {rule_id}."
            )

        seen_ids.add(rule_id)

        action = str(raw_rule.get("action", "")).upper()

        if action not in {"ALLOW", "DROP", "DENY"}:
            raise RuleValidationError(
                f"Rule {position}: action must be ALLOW, DROP, or DENY."
            )

        if action == "DENY":
            action = "DROP"

        protocol = str(
            raw_rule.get("protocol", "ANY")
        ).upper()

        if protocol not in {"TCP", "UDP", "ICMP", "ANY"}:
            raise RuleValidationError(
                f"Rule {position}: unsupported protocol '{protocol}'."
            )

        description = str(
            raw_rule.get("description", "")
        ).strip()

        source = str(
            raw_rule.get("source", "any")
        ).strip() or "any"

        destination = str(
            raw_rule.get("destination", "any")
        ).strip() or "any"

        enabled = raw_rule.get("enabled", True)

        if not isinstance(enabled, bool):
            raise RuleValidationError(
                f"Rule {position}: enabled must be true or false."
            )

        normalised.append(
            {
                "id": rule_id,
                "action": action,
                "protocol": protocol,
                "source": source,
                "destination": destination,
                "port": _normalise_port(
                    raw_rule.get("port", "any"),
                    position,
                ),
                "description": description,
                "enabled": enabled,
            }
        )

    return normalised


def load_policy(path: str | Path) -> list[dict[str, Any]]:
    """Load, parse and validate a JSON firewall policy."""

    policy_path = Path(path)

    if not policy_path.exists():
        raise FileNotFoundError(
            f"Policy file not found: {policy_path}"
        )

    if not policy_path.is_file():
        raise RuleValidationError(
            f"Policy path is not a file: {policy_path}"
        )

    try:
        with policy_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

    except json.JSONDecodeError as exc:
        raise RuleValidationError(
            "Policy file contains invalid JSON "
            f"at line {exc.lineno}, column {exc.colno}."
        ) from exc

    return validate_policy(data)