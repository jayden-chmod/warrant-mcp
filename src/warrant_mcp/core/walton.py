from typing import List, Optional, Tuple, Dict
from .types import ArgumentationScheme, CriticalQuestion

def create_scheme(
    name: str,
    major_premise: str,
    minor_premise: str,
    conclusion: str,
    cqs: List[Tuple[str, str]]
) -> ArgumentationScheme:
    questions = [
        CriticalQuestion(id=cq_id, question=q)
        for cq_id, q in cqs
    ]
    return ArgumentationScheme(
        name=name,
        majorPremise=major_premise,
        minorPremise=minor_premise,
        conclusion=conclusion,
        criticalQuestions=questions
    )

def expert_opinion() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Expert Opinion",
        "Source E is an expert in domain D containing proposition A.",
        "E asserts that proposition A is true (false).",
        "A may plausibly be taken to be true (false).",
        [
            ("CQ1", "How credible is E as an expert source?"),
            ("CQ2", "Is E an expert in the field that A is in?"),
            ("CQ3", "What did E assert that implies A?"),
            ("CQ4", "Is E personally reliable as a source?"),
            ("CQ5", "Is A consistent with what other experts assert?"),
            ("CQ6", "Is E's assertion based on evidence?")
        ]
    )

def position_to_know() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Position to Know",
        "Source a is in position to know about things in domain S containing proposition p.",
        "a asserts that p is true (false).",
        "p is true (false).",
        [
            ("CQ1", "Is a in position to know whether p is true (false)?"),
            ("CQ2", "Is a an honest (trustworthy, reliable) source?"),
            ("CQ3", "Did a assert that p is true (false)?")
        ]
    )

def practical_reasoning() -> ArgumentationScheme:
    return create_scheme(
        "Practical Reasoning",
        "Agent a has goal G.",
        "Carrying out action A is a means for a to realize G.",
        "Therefore, a ought to carry out action A.",
        [
            ("CQ1", "Are there alternative means to achieve G?"),
            ("CQ2", "Is A a feasible action?"),
            ("CQ3", "Are there unacceptable side effects of A?"),
            ("CQ4", "Does G conflict with other goals of a?")
        ]
    )

def consequences() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Consequences",
        "If action A is brought about, then consequence C will (may) occur.",
        "C is desirable (undesirable).",
        "Therefore, A should (should not) be brought about.",
        [
            ("CQ1", "How strong is the causal link between A and C?"),
            ("CQ2", "Are there other consequences of A besides C?"),
            ("CQ3", "Are the stated consequences truly desirable/undesirable?"),
            ("CQ4", "Could the consequences be prevented or mitigated?")
        ]
    )

def analogy() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Analogy",
        "Case C1 is similar to case C2.",
        "A is true in case C1.",
        "A is (plausibly) true in case C2.",
        [
            ("CQ1", "Are C1 and C2 truly similar in relevant respects?"),
            ("CQ2", "Are there critical differences that undermine the comparison?"),
            ("CQ3", "Is there a counterexample?")
        ]
    )

def popular_opinion() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Popular Opinion",
        "A large majority believes that A is true.",
        "If a large majority believes A, there is a presumption that A is true.",
        "There is a presumption that A is true.",
        [
            ("CQ1", "Is the claim about majority opinion well-founded?"),
            ("CQ2", "Even if popular, is there good reason to believe A false?")
        ]
    )

def sign() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Sign",
        "Event B is generally a sign of event A.",
        "B occurred in this case.",
        "Therefore, A occurred (or will occur) in this case.",
        [
            ("CQ1", "Is there a reliable correlation between A and B?"),
            ("CQ2", "Are there other plausible explanations for B?")
        ]
    )

def sunk_cost() -> ArgumentationScheme:
    return create_scheme(
        "Argument from Sunk Cost",
        "A large amount of resources has already been invested in project P.",
        "Abandoning P would waste the invested resources.",
        "Therefore, P should be continued.",
        [
            ("CQ1", "Are the sunk costs truly unrecoverable?"),
            ("CQ2", "Would continued investment lead to a positive outcome?"),
            ("CQ3", "Is the decision being driven by loss aversion rather than expected value?")
        ]
    )

SCHEMES = {
    "expert_opinion": expert_opinion,
    "position_to_know": position_to_know,
    "practical_reasoning": practical_reasoning,
    "consequences": consequences,
    "analogy": analogy,
    "popular_opinion": popular_opinion,
    "sign": sign,
    "sunk_cost": sunk_cost
}

def get_scheme(name: str) -> Optional[ArgumentationScheme]:
    factory = SCHEMES.get(name)
    return factory() if factory else None

def list_schemes() -> List[str]:
    return list(SCHEMES.keys())

def identify_scheme(claim: str, context: str) -> List[dict]:
    indicators = {
        "expert_opinion": ["expert", "authority", "research shows", "study", "according to"],
        "position_to_know": ["insider", "first-hand", "witnessed", "experienced"],
        "practical_reasoning": ["should", "ought to", "need to", "must", "goal", "in order to"],
        "consequences": ["will cause", "leads to", "results in", "consequence", "effect"],
        "analogy": ["similar to", "like", "just as", "same as", "comparable"],
        "popular_opinion": ["everyone", "most people", "commonly", "widely accepted"],
        "sign": ["indicates", "sign of", "symptom", "evidence of"],
        "sunk_cost": ["already invested", "wasted if", "come this far"]
    }
    
    combined = (claim + " " + context).lower()
    results = []
    
    for scheme, keywords in indicators.items():
        matches = [kw for kw in keywords if kw in combined]
        if matches:
            results.append({
                "scheme": scheme,
                "confidence": min(len(matches) / len(keywords), 1.0)
            })
            
    return sorted(results, key=lambda x: x["confidence"], reverse=True)
