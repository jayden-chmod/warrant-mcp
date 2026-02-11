from warrant_mcp.core.toulmin import (
    create_argument,
    validate_argument,
    score_argument,
    Evidence
)

def test_create_argument():
    arg = create_argument(
        claim="Harry is a British subject",
        data=["Harry was born in Bermuda"]
    )
    assert arg.claim == "Harry is a British subject"
    assert len(arg.data) == 1
    assert arg.qualifier == "presumably"

def test_create_argument_full():
    arg = create_argument(
        claim="Harry is a British subject",
        data=["Harry was born in Bermuda"],
        warrant="A man born in Bermuda will generally be a British subject",
        backing=["The following statutes..."],
        rebuttal=["Both his parents were aliens"],
        qualifier="presumably"
    )
    assert arg.warrant is not None
    assert len(arg.backing) == 1
    assert len(arg.rebuttal) == 1

def test_validate_argument():
    arg = create_argument(claim="X", data=["E"])
    res = validate_argument(arg)
    assert res.valid
    
    arg_inv = create_argument(claim="", data=["E"])
    res = validate_argument(arg_inv)
    assert not res.valid
    assert "Missing claim" in res.issues
    
    arg_inv2 = create_argument(claim="X", data=[])
    res = validate_argument(arg_inv2)
    assert not res.valid
    assert "Missing data" in res.issues

def test_argument_strength():
    arg = create_argument(
        claim="X",
        data=["E"],
        warrant="W",
        backing=["B"],
        rebuttal=["R"]
    )
    res = validate_argument(arg)
    assert res.strength == "strong"

def test_score_argument():
    arg = create_argument(
        claim="X",
        data=[Evidence(content="E1", type="certain")]
    )
    score = score_argument(arg)
    assert score.total > 0
    assert score.total <= 1.0
    
    # Check if certain evidence scores higher than uncertain
    arg_uncertain = create_argument(
        claim="X",
        data=[Evidence(content="E1", type="uncertain")]
    )
    score_uncertain = score_argument(arg_uncertain)
    assert score.total > score_uncertain.total
