from warrant_mcp.core.dung import (
    create_framework,
    is_conflict_free,
    is_admissible,
    grounded_extension,
    preferred_extensions,
    stable_extensions,
    get_attackers,
    get_attacked
)

def test_create_framework():
    af = create_framework([], [])
    assert af.arguments == set()
    assert af.attacks == set()

def test_lecture_example():
    # A = {a, b, c, d, e}, R = {(a,b),(b,c),(b,d),(e,b),(e,c)}
    af = create_framework(
        ["a", "b", "c", "d", "e"],
        [
            ("a", "b"),
            ("b", "c"),
            ("b", "d"),
            ("e", "b"),
            ("e", "c")
        ]
    )
    assert len(af.arguments) == 5
    assert len(af.attacks) == 5

def test_get_attackers():
    af = create_framework(["a", "b", "c"], [("a", "b"), ("c", "b")])
    assert get_attackers(af, "b") == {"a", "c"}
    assert get_attackers(af, "a") == set()

def test_get_attacked():
    af = create_framework(["a", "b", "c"], [("a", "b"), ("a", "c")])
    assert get_attacked(af, "a") == {"b", "c"}

def test_conflict_free():
    af = create_framework(["a", "b"], [("a", "b")])
    assert is_conflict_free(af, set())
    assert is_conflict_free(af, {"a"})
    
    af2 = create_framework(["a", "b"], [("a", "b"), ("b", "a")])
    assert not is_conflict_free(af2, {"a", "b"})

def test_admissible():
    # a -> b -> c : {a,c} is admissible because a defends c
    af = create_framework(["a", "b", "c"], [("a", "b"), ("b", "c")])
    assert is_admissible(af, {"a", "c"})
    
    # a -> b : {b} is not admissible
    af2 = create_framework(["a", "b"], [("a", "b")])
    assert not is_admissible(af2, {"b"})

def test_grounded_extension():
    # Chain a->b->c
    af = create_framework(
        ["a", "b", "c"],
        [("a", "b"), ("b", "c")]
    )
    # a is unattacked (accepted), b attacked by a (rejected), c attacked by b (defended by a) (accepted)
    assert grounded_extension(af) == {"a", "c"}
    
    # Mutual attack a <-> b
    af2 = create_framework(["a", "b"], [("a", "b"), ("b", "a")])
    assert grounded_extension(af2) == set()

def test_preferred_extensions():
    # Chain a->b->c
    af = create_framework(
        ["a", "b", "c"],
        [("a", "b"), ("b", "c")]
    )
    exts = preferred_extensions(af)
    assert len(exts) == 1
    assert exts[0] == {"a", "c"}
    
    # Mutual attack a <-> b
    af2 = create_framework(["a", "b"], [("a", "b"), ("b", "a")])
    exts = preferred_extensions(af2)
    assert len(exts) == 2
    # Check contents: one is {a}, one is {b}
    assert {"a"} in exts
    assert {"b"} in exts

def test_stable_extensions():
    # Chain a->b->c
    af = create_framework(
        ["a", "b", "c"],
        [("a", "b"), ("b", "c")]
    )
    stable = stable_extensions(af)
    assert len(stable) == 1
    assert stable[0] == {"a", "c"}
    
    # Self-attack a->a
    af2 = create_framework(["a"], [("a", "a")])
    assert len(stable_extensions(af2)) == 0
