"""Qualitative risk aggregation for analyzer findings."""

from __future__ import annotations

from collections import Counter
from typing import Any


SEVERITY_WEIGHTS = {
    "CRITICAL": 30,
    "HIGH": 20,
    "MEDIUM": 10,
    "LOW": 5,
}


def calculate_posture(
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate findings into a transparent posture result.

    The posture score is a project-defined analytical indicator.
    It is not a throughput benchmark or real-world security guarantee.
    """

    deduction = sum(
        SEVERITY_WEIGHTS.get(
            item.get("severity", "LOW"),
            0,
        )
        for item in findings
    )

    score = max(0, 100 - deduction)

    counts = Counter(
        item.get("severity", "UNKNOWN")
        for item in findings
    )

    if counts.get("CRITICAL", 0) or counts.get("HIGH", 0):
        posture = "HIGH RISK"

    elif counts.get("MEDIUM", 0):
        posture = "MODERATE RISK"

    elif counts.get("LOW", 0):
        posture = "LOW RISK"

    else:
        posture = "NO FINDINGS"

    return {
        "posture_score": score,
        "posture": posture,
        "finding_count": len(findings),
        "severity_counts": dict(counts),
    }