from typing import List, Dict, Union
from dataclasses import dataclass
from .types import DisagreementDiagnosis, DisagreementType

@dataclass
class AgentPosition:
    agent: str
    claim: str
    premises: List[str]
    rules: List[str]
    priorities: List[str]
    goals: List[str]

    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentPosition':
        return cls(
            agent=data.get("name") or data.get("agent", "unknown"),
            claim=data.get("claim", ""),
            premises=data.get("premises", []),
            rules=data.get("rules", []),
            priorities=data.get("priorities", []),
            goals=data.get("goals", [])
        )

def diagnose_disagreement(
    pos_a_data: Union[Dict, AgentPosition],
    pos_b_data: Union[Dict, AgentPosition]
) -> DisagreementDiagnosis:
    
    pos_a = pos_a_data if isinstance(pos_a_data, AgentPosition) else AgentPosition.from_dict(pos_a_data)
    pos_b = pos_b_data if isinstance(pos_b_data, AgentPosition) else AgentPosition.from_dict(pos_b_data)

    # Check if claims are compatible
    # Basic check: "not_X" vs "X"
    a_negated = pos_a.claim.startswith("not_")
    b_negated = pos_b.claim.startswith("not_")
    
    # If claim strings are different OR same string but different polarity (unlikely with just startswith not_)
    # Logic: if "A" vs "not_A", they conflict.
    # If "Use SQL" vs "Use NoSQL", they conflict (different strings, neither negated)
    
    # Let's align with TS logic:
    # const claimsConflict = posA.claim !== posB.claim || posA.claim.startsWith("not_") !== posB.claim.startsWith("not_");
    
    claims_conflict = (pos_a.claim != pos_b.claim) or (a_negated != b_negated)

    if not claims_conflict:
        # Same claim but different priorities
        priority_overlap = [p for p in pos_a.priorities if p in pos_b.priorities]
        min_len = min(len(pos_a.priorities), len(pos_b.priorities))
        
        if min_len > 0 and len(priority_overlap) < min_len:
            return DisagreementDiagnosis(
                type="preferential",
                description="Agents agree on the conclusion but disagree on what matters most.",
                resolution="Negotiate criteria weights or defer to stakeholder priorities.",
                agentA=pos_a.agent,
                agentB=pos_b.agent
            )

    # Check for goal conflicts
    goal_conflict = False
    for g in pos_a.goals:
        for g2 in pos_b.goals:
            # Check for direct negation "X" vs "not_X"
            g_clean = g.replace("not_", "")
            g2_clean = g2.replace("not_", "")
            if g_clean == g2_clean and (g.startswith("not_") != g2.startswith("not_")):
                goal_conflict = True
                break
        if goal_conflict:
            break
            
    if goal_conflict:
        return DisagreementDiagnosis(
            type="goal_conflict",
            description="Agents have fundamentally incompatible goals.",
            resolution="Escalate to human decision-maker. This cannot be resolved by further evidence or reasoning alone.",
            agentA=pos_a.agent,
            agentB=pos_b.agent
        )
        
    # Check for factual disagreement
    shared_premises = [p for p in pos_a.premises if p in pos_b.premises]
    max_len = max(len(pos_a.premises), len(pos_b.premises), 1)
    premise_overlap_ratio = len(shared_premises) / max_len
    
    if premise_overlap_ratio < 0.5:
        return DisagreementDiagnosis(
            type="factual",
            description="Agents are working from different evidence bases.",
            resolution="Share evidence and verify facts. The agent with stronger evidence should prevail.",
            agentA=pos_a.agent,
            agentB=pos_b.agent
        )
        
    return DisagreementDiagnosis(
        type="inferential",
        description="Agents share similar evidence but draw different conclusions due to different reasoning rules.",
        resolution="Examine the inference rules. Identify which rules are strict vs defeasible. The more specific rule typically takes priority.",
        agentA=pos_a.agent,
        agentB=pos_b.agent
    )

def suggest_resolution(diagnosis: DisagreementDiagnosis) -> List[str]:
    strategies = {
        "factual": [
            "Gather more evidence from authoritative sources",
            "Run experiments or benchmarks to verify disputed facts",
            "Check if evidence is outdated or context-dependent"
        ],
        "inferential": [
            "Make inference rules explicit and compare",
            "Identify which rules are defeasible vs strict",
            "Apply the specificity principle: more specific rules override general ones",
            "Check for undercutting defeaters that break the reasoning link"
        ],
        "preferential": [
            "Use multi-criteria decision matrix with agreed weights",
            "Identify which criteria are non-negotiable vs flexible",
            "Defer to the stakeholder whose domain is most affected"
        ],
        "goal_conflict": [
            "Escalate to human decision-maker",
            "Look for compromise solutions that partially satisfy both goals",
            "Reframe the problem to find superordinate goals",
            "Accept the trade-off and document the rationale"
        ]
    }
    
    return strategies.get(diagnosis.type, [])
