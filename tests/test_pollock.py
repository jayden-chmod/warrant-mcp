from warrant_mcp.core.pollock import (
    create_defeater,
    assess_strength
)

def test_classification():
    d = create_defeater("target", "content", "rebutting")
    assert d.type == "rebutting"
    
    d2 = create_defeater("target", "content", "undercutting")
    assert d2.type == "undercutting"

def test_strength():
    # Strong defeater: backed by certain evidence
    d = create_defeater("t", "c", "rebutting", "certain")
    assert assess_strength(d) == "strong"
    
    # Medium: objective
    d2 = create_defeater("t", "c", "rebutting", "objective")
    assert assess_strength(d2) == "medium"
    
    # Weak: subjective
    d3 = create_defeater("t", "c", "rebutting", "subjective")
    assert assess_strength(d3) == "weak"

def test_undercutting_stronger():
    # Undercutting defeaters are weighted higher
    rebutting = create_defeater("X", "not X", "rebutting", "objective")
    undercutting = create_defeater("X", "link broken", "undercutting", "objective")
    
    # We can check internal scores or just ensure strength category is at least as high
    # In the logic: rebutting(objective) -> 0.7 (borderline strong/medium? logic says >0.7 strong. 0.7 is medium >=0.35)
    # undercutting(objective) -> 0.7 * 1.2 = 0.84 -> Strong
    
    assert assess_strength(rebutting) == "medium"
    assert assess_strength(undercutting) == "strong"
