from warrant_mcp.core.gradual import (
    h_categorizer,
    counting_semantics,
    compute_scores
)
from warrant_mcp.core.dung import create_framework
from warrant_mcp.core.bipolar import create_bipolar_framework
import pytest

def test_h_categorizer():
    # Unattacked -> 1.0
    af = create_framework(["a"], [])
    scores = h_categorizer(af)
    assert scores["a"] == pytest.approx(1.0)
    
    # a -> b. a=1.0, b = 1/(1+1) = 0.5
    af2 = create_framework(["a", "b"], [("a", "b")])
    scores = h_categorizer(af2)
    assert scores["a"] == pytest.approx(1.0)
    assert scores["b"] == pytest.approx(0.5)
    
    # a -> b -> c. c should recover
    af3 = create_framework(["a", "b", "c"], [("a", "b"), ("b", "c")])
    scores = h_categorizer(af3)
    assert scores["a"] == pytest.approx(1.0)
    assert scores["b"] == pytest.approx(0.5)
    assert scores["c"] == pytest.approx(1.0 / (1.0 + 0.5)) # 0.666...

def test_counting():
    af = create_framework(["a"], [])
    scores = counting_semantics(af)
    assert scores["a"] > 0
    
    af2 = create_framework(["a", "b"], [("a", "b")])
    scores = counting_semantics(af2)
    assert scores["a"] > scores["b"]

def test_bipolar_scoring():
    # a supports b
    baf = create_bipolar_framework(["a", "b"], [], [("a", "b")])
    scores = compute_scores(baf)
    # support adds score
    assert scores["b"] > 1.0 
    assert scores["a"] == 1.0 # unattacked unsupported

def test_rational_postulates():
    # Adding an attacker decreases score
    af1 = create_framework(["a", "b"], [("a", "b")])
    af2 = create_framework(["a", "b", "c"], [("a", "b"), ("c", "b")])
    
    scores1 = h_categorizer(af1)
    scores2 = h_categorizer(af2)
    
    assert scores2["b"] < scores1["b"]
