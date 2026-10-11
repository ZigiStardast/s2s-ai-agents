"""Kontrolisani DSPy Reviewer, koji nije drugi autonomni agent."""

from __future__ import annotations

def review_finding(issue: str, root_cause: str, evidence: str):
    """Pozovi jedan dspy.Predict reviewer nad već dobijenim nalazom."""

    import dspy
    from .signatures import ReviewFinding

    reviewer = dspy.Predict(ReviewFinding)
    return reviewer(issue=issue, root_cause=root_cause, evidence=evidence)
