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

    # Format for agent-inbox
    request = {
        "action_request": {
            "action": "submit_decision",
            "args": {
                "claim_id": claim_id,
                "decision": decision,
                "coverage": coverage,
                "fraud_risk": fraud_risk,
                "damage_estimate": damage_estimate,
                "reason": reason,
            }
        },
        "config": {
            "allow_ignore": False,
            "allow_respond": True,
            "allow_edit": True,
            "allow_accept": True,
        },
        "description": f"""## Claim Triage Decision

**Claim ID:** {claim_id}

**Recommended Decision:** {decision}

| Field | Value |
|-------|-------|
| Coverage | {coverage} |
| Fraud Risk | {fraud_risk} |
| Damage Estimate | ${damage_estimate:,} |

**Reason:** {reason}
"""
    }

    response = interrupt(request)[0]

    if response["type"] == "accept":
        return f"Decision approved for {claim_id}: {decision}"
    elif response["type"] == "edit":
        edited = response.get("args", {})
        return f"Decision edited and approved for {claim_id}: {edited.get('decision', decision)}"
    elif response["type"] == "response":
        return f"Human responded: {response.get('args', '')}"
    elif response["type"] == "ignore":
        return f"Decision ignored for {claim_id}"

    return f"Decision processed for {claim_id}: {decision}"


TOOLS = [submit_decision]
