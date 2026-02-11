from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional, Any
from .core import dung, bipolar, gradual, toulmin, walton, pollock, prakken, aspic

mcp = FastMCP("warrant-mcp")

# Dialogue Session Store
dialogue_sessions = {}

# 1. Build Argument (Toulmin)
@mcp.tool()
def build_argument(
    claim: str,
    data: List[Dict[str, Any]], 
    warrant: Optional[str] = None,
    backing: Optional[List[str]] = None,
    rebuttal: Optional[List[str]] = None,
    qualifier: str = "presumably"
) -> Dict[str, Any]:
    """
    Build a structured argument using Toulmin's model.
    
    Args:
        claim: The assertion to be supported
        data: Evidence supporting the claim. Each item must have 'content' and 'type'.
        warrant: Why the data supports the claim
        backing: Evidence supporting the warrant
        rebuttal: Conditions under which the claim might not hold
        qualifier: Strength modifier (certainly, very likely, presumably, etc.)
    """
    arg = toulmin.create_argument(
        claim=claim,
        data=data,
        warrant=warrant,
        backing=backing,
        rebuttal=rebuttal,
        qualifier=qualifier
    )
    validation = toulmin.validate_argument(arg)
    score = toulmin.score_argument(arg)
    return {
        "argument": arg,
        "validation": validation,
        "score": score
    }

# 2. Identify Scheme
@mcp.tool()
def identify_scheme(
    claim: str,
    context: str = "",
    scheme: Optional[str] = None
) -> Dict[str, Any]:
    """Identify which Walton argumentation scheme matches a claim."""
    if scheme:
        s = walton.get_scheme(scheme)
        if not s:
            return {"error": f"Unknown scheme: {scheme}. Use list_schemes to see available schemes."}
        return s
        
    matches = walton.identify_scheme(claim, context)
    if not matches:
        return {
            "matches": [],
            "suggestion": "No scheme matched. Try providing more context or use list_schemes to pick one manually."
        }
        
    top_scheme = walton.get_scheme(matches[0]["scheme"])
    return {"matches": matches, "topScheme": top_scheme}

# 3. Classify Defeater
@mcp.tool()
def classify_defeater(
    target: str,
    content: str,
    type: str,
    evidence_type: str = "uncertain"
) -> Dict[str, Any]:
    """Classify a counterargument as rebutting or undercutting."""
    defeater = pollock.create_defeater(
        target=target,
        content=content,
        type=type, # casting string to DefeaterType
        evidence_type=evidence_type # casting string to EvidenceType
    )
    strength = pollock.assess_strength(defeater)
    penalty = pollock.defeater_penalty(defeater)
    return {
        "defeater": defeater,
        "strength": strength,
        "penalty": penalty
    }

# 4. Create Framework
@mcp.tool()
def create_framework(
    arguments: List[str],
    attacks: List[List[str]],
    supports: Optional[List[List[str]]] = None
) -> Dict[str, Any]:
    """Create a Dung Argumentation Framework or Bipolar AF."""
    # Convert list of lists to list of tuples
    attack_tuples = [(a[0], a[1]) for a in attacks]
    
    if supports:
        support_tuples = [(s[0], s[1]) for s in supports]
        baf = bipolar.create_bipolar_framework(arguments, attack_tuples, support_tuples)
        return {
            "type": "bipolar",
            "arguments": list(baf.arguments),
            "attacks": attacks,
            "supports": supports
        }
        
    af = dung.create_framework(arguments, attack_tuples)
    return {
        "type": "abstract",
        "arguments": list(af.arguments),
        "attacks": attacks
    }

# 5. Compute Extensions
@mcp.tool()
def compute_extensions(
    arguments: List[str],
    attacks: List[List[str]],
    semantics: str = "all"
) -> Dict[str, Any]:
    """Compute acceptable arguments using Dung's semantics."""
    attack_tuples = [(a[0], a[1]) for a in attacks]
    af = dung.create_framework(arguments, attack_tuples)
    result = {}
    
    if semantics in ["grounded", "all"]:
        ext = dung.grounded_extension(af)
        result["grounded"] = sorted(list(ext)) # Return as list (sorted for determinism)

    if semantics in ["preferred", "all"]:
        exts = dung.preferred_extensions(af)
        result["preferred"] = [sorted(list(e)) for e in exts]
        
    if semantics in ["stable", "all"]:
        exts = dung.stable_extensions(af)
        result["stable"] = [sorted(list(e)) for e in exts]
        
    return result

# 6. Score Arguments
@mcp.tool()
def score_arguments(
    arguments: List[str],
    attacks: List[List[str]],
    supports: Optional[List[List[str]]] = None,
    method: str = "h-categorizer"
) -> Dict[str, Any]:
    """Score arguments using gradual semantics."""
    attack_tuples = [(a[0], a[1]) for a in attacks]
    
    scores = {}
    
    if method == "bipolar" and supports:
        support_tuples = [(s[0], s[1]) for s in supports]
        baf = bipolar.create_bipolar_framework(arguments, attack_tuples, support_tuples)
        scores = gradual.compute_scores(baf)
    elif method == "counting":
        af = dung.create_framework(arguments, attack_tuples)
        scores = gradual.counting_semantics(af)
    else:
        af = dung.create_framework(arguments, attack_tuples)
        scores = gradual.h_categorizer(af)
        
    # Round scores
    result = {k: round(v, 3) for k, v in scores.items()}
    
    # Sort by score descending
    sorted_scores = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    
    return {
        "method": method,
        "scores": sorted_scores
    }

# 7. Create Dialogue
@mcp.tool()
def create_dialogue(
    topic: str,
    participants: List[str],
    type: str = "persuasion"
) -> Dict[str, Any]:
    """Start a new argumentation dialogue session."""
    d = prakken.create_dialogue(type, topic, participants)
    dialogue_sessions[d.id] = d
    return prakken.serialize_dialogue(d)

# 8. Dialogue Move
@mcp.tool()
def dialogue_move(
    dialogue_id: str,
    speaker: str,
    act: str,
    content: str,
    premises: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Make a speech act move in a dialogue."""
    d = dialogue_sessions.get(dialogue_id)
    if not d:
        raise ValueError(f"Dialogue not found: {dialogue_id}. Create one first.")
        
    move = prakken.SpeechAct(
        speaker=speaker,
        act=act,
        content=content,
        premises=premises
    )
    
    if not prakken.is_valid_move(d, move):
        last_move = d.moves[-1] if d.moves else None
        return {
            "error": "Invalid move according to Prakken's protocol",
            "move": move,
            "lastMove": last_move,
            "hint": "Check the protocol rules: claim->{why,claim,concede}, why->{since,retract}, since->{why,concede}"
        }
        
    new_d = prakken.make_move(d, move)
    dialogue_sessions[dialogue_id] = new_d
    return prakken.serialize_dialogue(new_d)

# 9. Diagnose Disagreement
@mcp.tool()
def diagnose_disagreement(
    agent_a: Dict[str, Any],
    agent_b: Dict[str, Any]
) -> Dict[str, Any]:
    """Diagnose WHY two agents disagree."""
    diagnosis = aspic.diagnose_disagreement(agent_a, agent_b)
    resolutions = aspic.suggest_resolution(diagnosis)
    return {
        "diagnosis": diagnosis,
        "suggestedResolutions": resolutions
    }

# 10. List Schemes
@mcp.tool()
def list_schemes() -> Dict[str, Any]:
    """List all available Walton argumentation schemes."""
    schemes = walton.list_schemes()
    details = []
    for name in schemes:
        s = walton.get_scheme(name)
        if s:
            details.append({
                "name": name,
                "title": s.name,
                "criticalQuestions": len(s.criticalQuestions)
            })
    return {"schemes": details}

def main():
    mcp.run()

if __name__ == "__main__":
    main()
