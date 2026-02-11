from typing import List, Optional, Union
from .types import ToulminArgument, Evidence, EvidenceType, QualifierLevel, ValidationResult, ScoreBreakdown

def create_argument(
    claim: str,
    data: List[Union[str, Evidence]],
    warrant: Optional[str] = None,
    backing: Optional[List[str]] = None,
    rebuttal: Optional[List[str]] = None,
    qualifier: QualifierLevel = "presumably"
) -> ToulminArgument:
    processed_data = []
    for d in data:
        if isinstance(d, str):
            processed_data.append(Evidence(content=d, type="uncertain"))
        elif isinstance(d, dict): # Handle dict input from MCP tools
            processed_data.append(Evidence(**d))
        else:
            processed_data.append(d)
            
    return ToulminArgument(
        claim=claim,
        data=processed_data,
        warrant=warrant,
        backing=backing,
        rebuttal=rebuttal,
        qualifier=qualifier
    )
    
def validate_argument(arg: ToulminArgument) -> ValidationResult:
    issues = []
    warnings = []
    
    if not arg.claim or not arg.claim.strip():
        issues.append("Missing claim")
        
    if not arg.data:
        issues.append("Missing data")
        
    if not arg.warrant:
        warnings.append("No warrant provided")
        
    if not arg.backing:
        warnings.append("No backing provided")
        
    if not arg.rebuttal:
        warnings.append("No rebuttals considered")
        
    strength = "weak"
    if issues:
        strength = "weak"
    elif arg.warrant and arg.backing and arg.rebuttal:
        strength = "strong"
    elif arg.warrant:
        strength = "moderate"
    else:
        strength = "weak"
        
    return ValidationResult(
        valid=len(issues) == 0,
        issues=issues,
        warnings=warnings,
        strength=strength
    )

EVIDENCE_WEIGHTS = {
    "certain": 0.1,
    "objective": 0.08,
    "uncertain": 0.05,
    "subjective": 0.03,
    "hypothetical": 0.02
}

def score_argument(arg: ToulminArgument) -> ScoreBreakdown:
    base = 0.3
    
    evidence_bonus = 0.0
    for evidence in arg.data:
        # evidence can be an object or dict depending on how it was created
        etype = evidence.type if hasattr(evidence, 'type') else evidence['type']
        evidence_bonus += EVIDENCE_WEIGHTS.get(etype, 0.03)
        
    warrant_bonus = 0.1 if arg.warrant else 0.0
    backing_bonus = min(len(arg.backing) * 0.05, 0.15) if arg.backing else 0.0
    rebuttal_penalty = 0.0
    
    numerator = base + evidence_bonus + warrant_bonus + backing_bonus - rebuttal_penalty
    total = min(max(numerator, 0.0), 1.0)
    
    return ScoreBreakdown(
        base=base,
        evidenceBonus=evidence_bonus,
        warrantBonus=warrant_bonus,
        backingBonus=backing_bonus,
        rebuttalPenalty=rebuttal_penalty,
        total=total
    )
