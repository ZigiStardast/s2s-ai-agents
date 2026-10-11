"""DSPy Signature klase koje se koriste u radionici."""

import dspy


class SummarizeIssue(dspy.Signature):
    """Summarize a software issue in one clear sentence."""

    issue: str = dspy.InputField()
    summary: str = dspy.OutputField()


class InvestigateIssue(dspy.Signature):
    """Investigate the issue with available evidence; do not guess the root cause."""

    issue: str = dspy.InputField()
    root_cause: str = dspy.OutputField()
    evidence: str = dspy.OutputField()
    recommendation: str = dspy.OutputField()


class ReviewFinding(dspy.Signature):
    """Decide whether a conclusion is adequately supported by the provided evidence."""

    issue: str = dspy.InputField()
    root_cause: str = dspy.InputField()
    evidence: str = dspy.InputField()
    verdict: str = dspy.OutputField(desc="Return SUPPORTED or NEED_MORE_EVIDENCE.")
    feedback: str = dspy.OutputField()
