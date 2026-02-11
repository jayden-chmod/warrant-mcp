from typing import Dict
from .types import ArgumentationFramework, BipolarFramework, decode_relation

def h_categorizer(
    af: ArgumentationFramework,
    max_iterations: int = 100,
    epsilon: float = 0.0001
) -> Dict[str, float]:
    scores = {arg: 1.0 for arg in af.arguments}
    
    for _ in range(max_iterations):
        max_delta = 0.0
        new_scores = {}
        
        for arg in af.arguments:
            attack_sum = 0.0
            for rel in af.attacks:
                from_node, to_node = decode_relation(rel)
                if to_node == arg:
                    attack_sum += scores[from_node]
            
            new_score = 1.0 / (1.0 + attack_sum)
            new_scores[arg] = new_score
            max_delta = max(max_delta, abs(new_score - scores[arg]))
            
        scores.update(new_scores)
        if max_delta < epsilon:
            break
            
    return scores

def count_paths(
    af: ArgumentationFramework,
    target: str,
    depth: int
) -> int:
    if depth == 0:
        return 1
        
    count = 0
    for rel in af.attacks:
        from_node, to_node = decode_relation(rel)
        if to_node == target:
            count += count_paths(af, from_node, depth - 1)
    return count

def counting_semantics(
    af: ArgumentationFramework,
    max_depth: int = 5
) -> Dict[str, float]:
    scores = {}
    
    for arg in af.arguments:
        score = 0.0
        for depth in range(max_depth + 1):
            paths = count_paths(af, arg, depth)
            sign = 1 if depth % 2 == 0 else -1
            score += sign * paths * (0.5 ** depth)
        scores[arg] = score
        
    return scores

def compute_scores(
    baf: BipolarFramework,
    max_iterations: int = 100,
    epsilon: float = 0.0001
) -> Dict[str, float]:
    scores = {arg: 1.0 for arg in baf.arguments}
    
    for _ in range(max_iterations):
        max_delta = 0.0
        new_scores = {}
        
        for arg in baf.arguments:
            attack_sum = 0.0
            for rel in baf.attacks:
                from_node, to_node = decode_relation(rel)
                if to_node == arg:
                    attack_sum += scores[from_node]
            
            support_sum = 0.0
            for rel in baf.supports:
                from_node, to_node = decode_relation(rel)
                if to_node == arg:
                    support_sum += scores[from_node] * 0.5
            
            new_score = min((1.0 + support_sum) / (1.0 + attack_sum), 2.0)
            new_scores[arg] = new_score
            max_delta = max(max_delta, abs(new_score - scores[arg]))
            
        scores.update(new_scores)
        if max_delta < epsilon:
            break
            
    return scores
