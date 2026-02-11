from typing import Set, List, Tuple
from .types import ArgumentationFramework, encode_relation, decode_relation

def create_framework(
    args: List[str],
    attacks: List[Tuple[str, str]]
) -> ArgumentationFramework:
    return ArgumentationFramework(
        arguments=set(args),
        attacks={encode_relation(a, b) for a, b in attacks}
    )

def get_attackers(af: ArgumentationFramework, arg: str) -> Set[str]:
    result = set()
    for rel in af.attacks:
        from_node, to_node = decode_relation(rel)
        if to_node == arg:
            result.add(from_node)
    return result

def get_attacked(af: ArgumentationFramework, arg: str) -> Set[str]:
    result = set()
    for rel in af.attacks:
        from_node, to_node = decode_relation(rel)
        if from_node == arg:
            result.add(to_node)
    return result

def attacks(af: ArgumentationFramework, a: str, b: str) -> bool:
    return encode_relation(a, b) in af.attacks

def is_conflict_free(af: ArgumentationFramework, s: Set[str]) -> bool:
    for a in s:
        for b in s:
            if attacks(af, a, b):
                return False
    return True

def defends(af: ArgumentationFramework, s: Set[str], arg: str) -> bool:
    for attacker in get_attackers(af, arg):
        defended = False
        for defender in s:
            if attacks(af, defender, attacker):
                defended = True
                break
        if not defended:
            return False
    return True

def is_admissible(af: ArgumentationFramework, s: Set[str]) -> bool:
    if not is_conflict_free(af, s):
        return False
    for arg in s:
        if not defends(af, s, arg):
            return False
    return True

def grounded_extension(af: ArgumentationFramework) -> Set[str]:
    current = set()
    while True:
        next_set = set()
        for arg in af.arguments:
            if defends(af, current, arg):
                next_set.add(arg)
        if current == next_set:
            break
        current = next_set
    return current

def power_set(s: Set[str]) -> List[Set[str]]:
    arr = list(s)
    result = []
    total = 1 << len(arr)
    for i in range(total):
        subset = set()
        for j in range(len(arr)):
            if i & (1 << j):
                subset.add(arr[j])
        result.append(subset)
    return result

def find_all_admissible(af: ArgumentationFramework) -> List[Set[str]]:
    result = []
    for subset in power_set(af.arguments):
        if is_admissible(af, subset):
            result.append(subset)
    return result

def preferred_extensions(af: ArgumentationFramework) -> List[Set[str]]:
    admissible = find_all_admissible(af)
    maximal = []
    
    for s in admissible:
        is_maximal = True
        for other in admissible:
            if other != s and s.issubset(other) and s != other:
                is_maximal = False
                break
        if is_maximal:
            maximal.append(s)
            
    return maximal

def stable_extensions(af: ArgumentationFramework) -> List[Set[str]]:
    result = []
    all_subsets = power_set(af.arguments)
    
    for subset in all_subsets:
        if not is_conflict_free(af, subset):
            continue
            
        is_stable = True
        for arg in af.arguments:
            if arg in subset:
                continue
            attacked = False
            for member in subset:
                if attacks(af, member, arg):
                    attacked = True
                    break
            if not attacked:
                is_stable = False
                break
        if is_stable:
            result.append(subset)
            
    return result
