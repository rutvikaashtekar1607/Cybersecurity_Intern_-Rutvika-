"""Run the CyberOS Week 3 posture-analysis pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.risk_analyzer import analyze_rules
from src.rule_parser import load_policy
from src.scorer import calculate_posture


def run(
    input_path: Path,
    output_path: Path,
) -> dict:

    rules = load_policy(input_path)

    findings = analyze_rules(rules)

    posture = calculate_posture(findings)

    result = {
        "input_file": str(input_path),
        "rules_analyzed": len(rules),
        "findings": findings,
        **posture,
    }

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    return result


def main() -> int:

    input_path = (
        PROJECT_ROOT
        / "sample_data"
        / "firewall_rules.json"
    )

    output_path = (
        PROJECT_ROOT
        / "results"
        / "scan_results.json"
    )

    try:
        result = run(
            input_path,
            output_path,
        )

    except (OSError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(
        "CyberOS Firewall Security Posture Analyzer"
    )
    print("-------------------------------------------")
    print(
        f"Rules analyzed : {result['rules_analyzed']}"
    )
    print(
        f"Findings       : {result['finding_count']}"
    )
    print(
        f"Posture        : {result['posture']}"
    )
    print(
        f"Posture score  : "
        f"{result['posture_score']}/100"
    )
    print(
        f"Results saved  : {output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())