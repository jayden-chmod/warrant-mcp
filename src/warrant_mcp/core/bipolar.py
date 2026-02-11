from typing import Set, List, Tuple
from .types import BipolarFramework, encode_relation, decode_relation

def create_bipolar_framework(
    args: List[str],
    attacks: List[Tuple[str, str]],
    supports: List[Tuple[str, str]]
) -> BipolarFramework:
    return BipolarFramework(
        arguments=set(args),
        attacks={encode_relation(a, b) for a, b in attacks},
        supports={encode_relation(a, b) for a, b in supports}
    )

def get_supporters(baf: BipolarFramework, arg: str) -> Set[str]:
    result = set()
    for rel in baf.supports:
        from_node, to_node = decode_relation(rel)
        if to_node == arg:
            result.add(from_node)
    return result

def get_supported(baf: BipolarFramework, arg: str) -> Set[str]:
    result = set()
    for rel in baf.supports:
        from_node, to_node = decode_relation(rel)
        if from_node == arg:
            result.add(to_node)
    return result

def get_attackers(baf: BipolarFramework, arg: str) -> Set[str]:
    result = set()
    for rel in baf.attacks:
        from_node, to_node = decode_relation(rel)
        if to_node == arg:
            result.add(from_node)
    return result

def get_supported_attacks(
    baf: BipolarFramework,
    arg: str
) -> List[dict]:
    result = []
    # A supports B, B attacks arg -> A indirectly attacks arg
    for rel in baf.attacks:
        direct_attacker, target = decode_relation(rel)
        if target != arg:
            continue
        for supporter in get_supporters(baf, direct_attacker):
            result.append({"attacker": supporter, "via": direct_attacker})
    return result

def get_secondary_attacks(
    baf: BipolarFramework,
    arg: str
) -> List[dict]:
    result = []
    for supporter in get_supporters(baf, arg):
        for rel in baf.attacks:
            attacker, target = decode_relation(rel)
            if target == supporter:
                result.append({"attacker": attacker, "via": supporter})
    return result

def flatten_to_af(baf: BipolarFramework) -> BipolarFramework:
    new_attacks = set(baf.attacks)
    
    for arg in baf.arguments:
        for sa in get_supported_attacks(baf, arg):
            new_attacks.add(encode_relation(sa["attacker"], arg))
        for sa in get_secondary_attacks(baf, arg):
            new_attacks.add(encode_relation(sa["attacker"], arg))
            
    return BipolarFramework(
        arguments=set(baf.arguments),
        attacks=new_attacks,
        supports=set(baf.supports)
    )
