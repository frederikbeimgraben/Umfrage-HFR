"""
Tools for creating surveys
"""

from typing import Any, Dict, List
import json
import os

KEEP = [-1, -1]

ZERO = [
    [0, 0],
    [0, 0]
]

COUNTER = 1

TARGETS = [
    {
        "name": "Regie",
        "states": 3
    },
    {
        "name": "Pacht",
        "states": 3
    }
]

def Option(text: str, scores: List[List[int]], next_states: List[int]=KEEP, targets: List=TARGETS) -> Dict[str, Any]:
    """
    Make an option with the given text, scores and next states
    """
    
    # if scores is one-dimensional, make it two-dimensional
    for i, score in enumerate(scores):
        if not isinstance(score, list):
            scores[i] = [score] * TARGETS[i]["states"]
        
    
    return {
        "text": text,
        "scores": scores,
        "next_states": next_states
    }
    
def OptionT(targets: List) -> callable:
    def innerOption(text: str, scores: List[List[int]], next_states: List[int]=KEEP) -> Dict[str, Any]:
        return Option(text, scores, next_states, targets)
    
    return innerOption

def Question(text: str, options: List[Any], title: str=None) -> Dict[str, Any]:
    """
    Make a question with the given text and options
    """
    
    global COUNTER
    
    question = {
        "title": f"Frage {COUNTER}" if title is None else title,
        "text": text,
        "options": options + [
            Option("Keine Angabe", ZERO)
        ]
    }
    
    COUNTER += 1
    
    return question

AGREE = "Stimme zu"
AGREE_PARTLY = "Stimme teilweise zu"
NEUTRAL = "Neutral"
DISAGREE_PARTLY = "Stimme teilweise nicht zu"
DISAGREE = "Stimme nicht zu"

DEFAULT_SET_A = [
    Option(AGREE,    [2, 0]),
    Option(NEUTRAL,  [1, 1]),
    Option(DISAGREE, [0, 2])
]

DEFAULT_SET_B = [
    Option(AGREE,    [0, 2]),
    Option(NEUTRAL,  [1, 1]),
    Option(DISAGREE, [2, 0])
]

DEFAULT_2D_APPD_A = [
    Option(AGREE,           [[3, 0], [0, 3]]),
    Option(AGREE_PARTLY,    [[2, 1], [1, 2]]),
    Option(DISAGREE_PARTLY, [[1, 2], [2, 1]]),
    Option(DISAGREE,        [[0, 3], [3, 0]])
]

DEFAULT_2D_APPD_B = [
    Option(AGREE,           [[0, 3], [3, 0]]),
    Option(AGREE_PARTLY,    [[1, 2], [2, 1]]),
    Option(DISAGREE_PARTLY, [[2, 1], [1, 2]]),
    Option(DISAGREE,        [[3, 0], [0, 3]])
]

DEFAULT_2D_AND_A = [
    Option(AGREE,           [[2, 0], [0, 2]]),
    Option(NEUTRAL,         [[1, 1], [1, 1]]),
    Option(DISAGREE,        [[0, 2], [2, 0]])
]

DEFAULT_2D_AND_B = [
    Option(AGREE,           [[0, 2], [2, 0]]),
    Option(NEUTRAL,         [[1, 1], [1, 1]]),
    Option(DISAGREE,        [[2, 0], [0, 2]])
]