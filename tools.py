"""Tools for the insurance claims triage agent."""

import json
import os
from typing import Annotated, Literal

CLAIMS_DIR = os.path.join(os.path.dirname(__file__), "claims")
PROCESSED_FILE = os.path.join(os.path.dirname(__file__), "processed_claims.json")


def _load_processed() -> set:
    """Load set of processed claim IDs."""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE) as f:
            return set(json.load(f))
    return set()


def _save_processed(processed: set):
    """Save processed claim IDs."""
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed), f)


def get_pending_claims() -> str:
    """Get all pending claims that haven't been processed yet."""
    processed = _load_processed()
    pending = []

    for claim_dir in os.listdir(CLAIMS_DIR):
        claim_path = os.path.join(CLAIMS_DIR, claim_dir, "claim.json")
        if os.path.exists(claim_path):
            with open(claim_path) as f:
                claim = json.load(f)
                if claim["claim_id"] not in processed:
                    pending.append(claim)

    if not pending:
        return "No pending claims to process."

    return json.dumps(pending, indent=2)


def mark_claim_processed(
    claim_id: Annotated[str, "The claim ID to mark as processed"],
) -> str:
    """Mark a claim as processed after triage is complete."""
    processed = _load_processed()
    processed.add(claim_id)
    _save_processed(processed)
    return f"Claim {claim_id} marked as processed."


def submit_decision(
    claim_id: Annotated[str, "The claim ID this decision is for"],
    decision: Annotated[Literal["AUTO-APPROVE", "DENY", "MANUAL REVIEW"], "The triage decision"],
    coverage: Annotated[str, "Coverage status (yes/no)"],
    fraud_risk: Annotated[str, "Fraud risk level (low/high)"],
    damage_estimate: Annotated[int, "Estimated damage in dollars"],
    reason: Annotated[str, "One sentence explanation"],
) -> str:
    """Submit the final triage decision. MANUAL REVIEW decisions require human approval."""
    return f"Decision submitted for {claim_id}: {decision}"


TOOLS = [get_pending_claims, mark_claim_processed, submit_decision]
