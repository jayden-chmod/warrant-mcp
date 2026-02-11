import time
from typing import List, Optional, Set, Dict, Any
from .types import DialogueState, SpeechAct, DialogueType, SpeechActType

_dialogue_counter = 0

def create_dialogue(
    type: DialogueType,
    topic: str,
    participants: List[str]
) -> DialogueState:
    global _dialogue_counter
    _dialogue_counter += 1
    
    commitments = {p: set() for p in participants}
    
    return DialogueState(
        id=f"dialogue_{_dialogue_counter}",
        type=type,
        topic=topic,
        participants=participants,
        moves=[],
        commitments=commitments
    )

def get_commitments(state: DialogueState, participant: str) -> Set[str]:
    return state.commitments.get(participant, set())

PROTOCOL = {
    "claim": ["why", "claim", "concede"],
    "why": ["since", "retract"],
    "concede": [],
    "retract": [],
    "since": ["why", "concede"],
    "question": ["claim", "retract"]
}

def is_valid_move(state: DialogueState, move: SpeechAct) -> bool:
    if not state.moves:
        return move.act in ["claim", "question"]
        
    if move.speaker not in state.participants:
        return False
        
    last_move = state.moves[-1]
    valid_responses = PROTOCOL.get(last_move.act, [])
    
    if not valid_responses:
        return move.act in ["claim", "question"]
        
    return move.act in valid_responses

def make_move(state: DialogueState, move: SpeechAct) -> DialogueState:
    new_commitments = {k: set(v) for k, v in state.commitments.items()}
    store = new_commitments.get(move.speaker, set())
    
    if move.act == "claim":
        store.add(move.content)
    elif move.act == "concede":
        store.add(move.content)
    elif move.act == "retract":
        if move.content in store:
            store.remove(move.content)
    elif move.act == "since":
        store.add(move.content)
        if move.premises:
            for p in move.premises:
                store.add(p)
                
    new_commitments[move.speaker] = store
    
    new_move = SpeechAct(
        speaker=move.speaker,
        act=move.act,
        content=move.content,
        premises=move.premises,
        # Use simple integer timestamp or None for testing consistency
        timestamp=int(time.time() * 1000)
    )
    
    return DialogueState(
        id=state.id,
        type=state.type,
        topic=state.topic,
        participants=state.participants,
        moves=state.moves + [new_move],
        commitments=new_commitments
    )
    
def serialize_dialogue(state: DialogueState) -> Dict[str, Any]:
    commitments = {k: list(v) for k, v in state.commitments.items()}
    moves = []
    for m in state.moves:
        moves.append({
            "speaker": m.speaker,
            "act": m.act,
            "content": m.content,
            "premises": m.premises,
            "timestamp": m.timestamp
        })
        
    return {
        "id": state.id,
        "type": state.type,
        "topic": state.topic,
        "participants": state.participants,
        "moves": moves,
        "commitments": commitments,
        "moveCount": len(state.moves)
    }
