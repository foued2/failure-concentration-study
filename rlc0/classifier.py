import json


LABELS = (
    "NO_FAILURE",
    "REFUTED",
    "CERTIFIED_LOCALIZED",
    "CANDIDATE_ONLY",
    "UNKNOWN",
)


def classify(evidence):
    if evidence.get("full_d_proof") == "complete":
        return "NO_FAILURE"
    if evidence.get("outside_f_failure_verified") is True:
        return "REFUTED"
    if evidence.get("in_f_failure_verified") is True:
        if evidence.get("d_f_proof") == "complete":
            return "CERTIFIED_LOCALIZED"
        return "CANDIDATE_ONLY"
    return "UNKNOWN"


def classify_all(evidence_by_seed):
    return {seed_id: classify(evidence) for seed_id, evidence in evidence_by_seed.items()}
