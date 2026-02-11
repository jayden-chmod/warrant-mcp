from typing import Optional
from .types import Defeater, DefeaterType, EvidenceType, DefeaterStrength

def create_defeater(
    target: str,
    content: str,
    type: DefeaterType,
    evidence_type: EvidenceType = "uncertain"
) -> Defeater:
    return Defeater(
        target=target,
        content=content,
        type=type,
        evidenceType=evidence_type
    )

def assess_strength(defeater: Defeater) -> DefeaterStrength:
    evidence_strength = {
        "certain": 1.0,
        "objective": 0.7,
        "uncertain": 0.4,
        "subjective": 0.2,
        "hypothetical": 0.1
    }
    
    base = evidence_strength.get(defeater.evidenceType, 0.4)
    type_multiplier = 1.2 if defeater.type == "undercutting" else 1.0
    score = base * type_multiplier
    
    if score > 0.7:
        return "strong"
    if score >= 0.35:
        return "medium"
    return "weak"

def defeater_penalty(defeater: Defeater) -> float:
    strength_penalty = {
        "strong": 0.15,
        "medium": 0.08,
        "weak": 0.03
    }
    
    strength = assess_strength(defeater)
    base = strength_penalty[strength]
    
    return base * 1.3 if defeater.type == "undercutting" else base
