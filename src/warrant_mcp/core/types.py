from dataclasses import dataclass
from typing import Literal, Set, List, Optional, Tuple, Dict

# Dung's Abstract Argumentation Framework

@dataclass
class ArgumentationFramework:
    arguments: Set[str]
    # Stored as "attacker->target" for Set compatibility
    attacks: Set[str]

# Bipolar AF (Attack + Support)

@dataclass
class BipolarFramework(ArgumentationFramework):
    # Stored as "supporter->supported" strings
    supports: Set[str]

# Toulmin Model

EvidenceType = Literal[
    "certain",
    "objective",
    "uncertain",
    "subjective",
    "hypothetical"
]

QualifierLevel = Literal[
    "certainly",
    "very likely",
    "presumably",
    "probably",
    "possibly",
    "uncertain"
]

@dataclass
class Evidence:
    content: str
    type: EvidenceType
    source: Optional[str] = None

@dataclass
class ToulminArgument:
    claim: str
    data: List[Evidence]
    warrant: Optional[str] = None
    backing: Optional[List[str]] = None
    rebuttal: Optional[List[str]] = None
    qualifier: QualifierLevel = "presumably"

@dataclass
class ValidationResult:
    valid: bool
    issues: List[str]
    warnings: List[str]
    strength: Literal["strong", "moderate", "weak"]

@dataclass
class ScoreBreakdown:
    base: float
    evidenceBonus: float
    warrantBonus: float
    backingBonus: float
    rebuttalPenalty: float
    total: float

# Pollock's Defeaters

DefeaterType = Literal["rebutting", "undercutting"]
DefeaterStrength = Literal["strong", "medium", "weak"]

@dataclass
class Defeater:
    target: str
    content: str
    type: DefeaterType
    evidenceType: EvidenceType
    strength: Optional[DefeaterStrength] = None

# Walton's Schemes

@dataclass
class CriticalQuestion:
    id: str
    question: str
    answer: Optional[str] = None
    satisfied: Optional[bool] = None

@dataclass
class ArgumentationScheme:
    name: str
    majorPremise: str
    minorPremise: str
    conclusion: str
    criticalQuestions: List[CriticalQuestion]

# Prakken's Dialogue

DialogueType = Literal[
    "persuasion",
    "negotiation",
    "inquiry",
    "deliberation",
    "information_seeking"
]

SpeechActType = Literal[
    "claim",
    "why",
    "concede",
    "retract",
    "since",
    "question"
]

@dataclass
class SpeechAct:
    speaker: str
    act: SpeechActType
    content: str
    premises: Optional[List[str]] = None
    timestamp: Optional[int] = None

@dataclass
class DialogueState:
    id: str
    type: DialogueType
    topic: str
    participants: List[str]
    moves: List[SpeechAct]
    commitments: Dict[str, Set[str]]

# ASPIC+ Disagreement

DisagreementType = Literal[
    "factual",
    "inferential",
    "preferential",
    "goal_conflict"
]

@dataclass
class DisagreementDiagnosis:
    type: DisagreementType
    description: str
    resolution: str
    agentA: str
    agentB: str

# Attack/Support encoding helpers

def encode_relation(from_node: str, to_node: str) -> str:
    return f"{from_node}->{to_node}"

def decode_relation(rel: str) -> Tuple[str, str]:
    parts = rel.split("->")
    return (parts[0], parts[1])
