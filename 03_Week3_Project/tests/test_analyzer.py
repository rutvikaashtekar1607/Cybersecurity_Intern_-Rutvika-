"""Tests for the Week 3 firewall posture analyzer."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.risk_analyzer import analyze_rules
from src.rule_parser import (
    RuleValidationError,
    load_policy,
    validate_policy,
)
from src.scorer import calculate_posture


def valid_policy():
    return {
        "rules": [
            {
                "id": 1,
                "action": "ALLOW",
                "protocol": "TCP",
                "source": "10.0.0.0/24",
                "destination": "10.0.1.10",
                "port": 443,
                "description": "HTTPS",
            }
        ]
    }


# -------------------------
# Functional tests
# -------------------------


def test_01_parser_accepts_valid_policy():
    result = validate_policy(valid_policy())

    assert result[0]["port"] == 443


def test_02_parser_applies_default_scope():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "DROP",
                "protocol": "TCP",
                "port": 0,
            }
        ]
    }

    rule = validate_policy(policy)[0]

    assert rule["source"] == "any"
    assert rule["destination"] == "any"


def test_03_parser_normalises_lowercase_values():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "allow",
                "protocol": "tcp",
                "port": 80,
            }
        ]
    }

    rule = validate_policy(policy)[0]

    assert rule["action"] == "ALLOW"
    assert rule["protocol"] == "TCP"


def test_04_parser_supports_any_port():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "DROP",
                "protocol": "ANY",
                "port": "any",
            }
        ]
    }

    assert validate_policy(policy)[0]["port"] == "any"


def test_05_detects_overly_permissive_rule():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "ALLOW",
                "protocol": "TCP",
                "port": "any",
            }
        ]
    }

    findings = analyze_rules(
        validate_policy(policy)
    )

    assert any(
        item["finding_id"] == "F-001"
        for item in findings
    )


def test_06_detects_sensitive_port_exposure():
    policy = {
        "rules": [
            {
                "id": 2,
                "action": "ALLOW",
                "protocol": "TCP",
                "port": 22,
            }
        ]
    }

    findings = analyze_rules(
        validate_policy(policy)
    )

    assert any(
        item["finding_id"] == "F-002"
        for item in findings
    )


def test_07_detects_any_protocol():
    policy = {
        "rules": [
            {
                "id": 3,
                "action": "ALLOW",
                "protocol": "ANY",
                "port": 443,
            }
        ]
    }

    findings = analyze_rules(
        validate_policy(policy)
    )

    assert any(
        item["finding_id"] == "F-003"
        for item in findings
    )


def test_08_ignores_disabled_rule():
    policy = {
        "rules": [
            {
                "id": 4,
                "action": "ALLOW",
                "protocol": "TCP",
                "port": "any",
                "enabled": False,
            }
        ]
    }

    assert analyze_rules(
        validate_policy(policy)
    ) == []


def test_09_drop_rule_has_no_allow_finding():
    policy = {
        "rules": [
            {
                "id": 5,
                "action": "DROP",
                "protocol": "ANY",
                "port": "any",
            }
        ]
    }

    assert analyze_rules(
        validate_policy(policy)
    ) == []


def test_10_loads_sample_policy():
    sample = (
        PROJECT_ROOT
        / "sample_data"
        / "firewall_rules.json"
    )

    rules = load_policy(sample)

    assert len(rules) == 4


# -------------------------
# Negative / security tests
# -------------------------


def test_11_rejects_non_object_policy():
    with pytest.raises(RuleValidationError):
        validate_policy([])


def test_12_rejects_missing_rules():
    with pytest.raises(RuleValidationError):
        validate_policy({})


def test_13_rejects_invalid_action():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "EXECUTE",
                "protocol": "TCP",
                "port": 80,
            }
        ]
    }

    with pytest.raises(RuleValidationError):
        validate_policy(policy)


def test_14_rejects_invalid_protocol():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "ALLOW",
                "protocol": "TELNET",
                "port": 80,
            }
        ]
    }

    with pytest.raises(RuleValidationError):
        validate_policy(policy)


def test_15_rejects_invalid_port():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "ALLOW",
                "protocol": "TCP",
                "port": 70000,
            }
        ]
    }

    with pytest.raises(RuleValidationError):
        validate_policy(policy)


# -------------------------
# Failure / edge-case tests
# -------------------------


def test_16_rejects_duplicate_rule_ids():
    policy = {
        "rules": [
            {
                "id": 1,
                "action": "ALLOW",
                "protocol": "TCP",
                "port": 80,
            },
            {
                "id": 1,
                "action": "DROP",
                "protocol": "TCP",
                "port": 80,
            },
        ]
    }

    with pytest.raises(RuleValidationError):
        validate_policy(policy)


def test_17_rejects_malformed_json(tmp_path):
    path = tmp_path / "broken.json"

    path.write_text(
        '{"rules": [}',
        encoding="utf-8",
    )

    with pytest.raises(RuleValidationError):
        load_policy(path)


def test_18_rejects_missing_input_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_policy(
            tmp_path / "missing.json"
        )


def test_19_empty_findings_produce_no_findings_state():
    result = calculate_posture([])

    assert result["posture"] == "NO FINDINGS"
    assert result["posture_score"] == 100