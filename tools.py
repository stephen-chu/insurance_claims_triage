"""Tools for the insurance claims triage agent."""

from typing import Annotated, Literal
from langgraph.types import interrupt


def submit_decision(
    claim_id: Annotated[str, "The claim ID this decision is for"],
    decision: Annotated[Literal["AUTO-APPROVE", "DENY", "MANUAL REVIEW"], "The triage decision"],
    coverage: Annotated[str, "Coverage status (yes/no)"],
    fraud_risk: Annotated[str, "Fraud risk level (low/high)"],
    damage_estimate: Annotated[int, "Estimated damage in dollars"],
    reason: Annotated[str, "One sentence explanation"],
) -> str:
    """Submit the final triage decision. Pauses for human review."""
    # Interrupt and wait for human approval
    human_review = interrupt({
        "claim_id": claim_id,
        "decision": decision,
        "coverage": coverage,
        "fraud_risk": fraud_risk,
        "damage_estimate": damage_estimate,
        "reason": reason,
    })

    # Human can approve, edit, or reject
    if human_review.get("action") == "reject":
        return f"Decision rejected by reviewer: {human_review.get('feedback', 'No feedback')}"

    # Use edited values if provided, otherwise use original
    final_decision = human_review.get("decision", decision)
    return f"Decision approved for {claim_id}: {final_decision}"


TOOLS = [submit_decision]
