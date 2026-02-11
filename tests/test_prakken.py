from warrant_mcp.core.prakken import (
    create_dialogue,
    make_move,
    is_valid_move,
    get_commitments,
    SpeechAct
)

def test_create_dialogue():
    d = create_dialogue("persuasion", "topic", ["Paul", "Olga"])
    assert d.type == "persuasion"
    assert len(d.moves) == 0
    assert get_commitments(d, "Paul") == set()

def test_speech_acts_and_effects():
    d = create_dialogue("persuasion", "topic", ["P", "O"])
    
    # Claim adds to commitment
    d = make_move(d, SpeechAct("P", "claim", "safe"))
    assert "safe" in get_commitments(d, "P")
    
    # Why does not change commitment
    d = make_move(d, SpeechAct("O", "why", "safe"))
    assert "safe" not in get_commitments(d, "O")
    
    # Since adds conclusion and premises
    d = make_move(d, SpeechAct("P", "since", "safe", ["airbag"]))
    assert "safe" in get_commitments(d, "P")
    assert "airbag" in get_commitments(d, "P")

def test_protocol_compliance():
    d = create_dialogue("persuasion", "topic", ["P", "O"])
    
    # First move must be claim or question
    assert is_valid_move(d, SpeechAct("P", "claim", "safe"))
    assert not is_valid_move(d, SpeechAct("P", "why", "safe"))
    
    # Make claim
    d = make_move(d, SpeechAct("P", "claim", "safe"))
    
    # Valid responses to claim: why, claim, concede
    assert is_valid_move(d, SpeechAct("O", "why", "safe"))
    assert is_valid_move(d, SpeechAct("O", "concede", "safe"))
    
    # Invalid response
    assert not is_valid_move(d, SpeechAct("O", "since", "safe"))

def test_full_dialogue_replay():
    d = create_dialogue("persuasion", "safe", ["Paul", "Olga"])
    
    # P1: claim safe
    d = make_move(d, SpeechAct("Paul", "claim", "safe"))
    
    # O2: why safe
    d = make_move(d, SpeechAct("Olga", "why", "safe"))
    
    # P3: safe since airbag
    d = make_move(d, SpeechAct("Paul", "since", "safe", ["airbag"]))
    assert "airbag" in get_commitments(d, "Paul")
    
    # O4: concede airbag
    d = make_move(d, SpeechAct("Olga", "concede", "airbag"))
    assert "airbag" in get_commitments(d, "Olga")
    
    assert len(d.moves) == 4
