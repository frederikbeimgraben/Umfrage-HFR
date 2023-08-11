#!/usr/bin/env python3
"""
Generates a JSON file from itself
"""

from typing import Any, Dict, List
import json
import os

TARGETS = [
    {
        "name": "Endlich Fertig!",
        "states": 1
    },
    {
        "name": "Ich bin grau :(",
        "states": 1
    }
]

KEEP = [-1, -1]

ZERO = [
    [0, 0],
    [0, 0]
]

COUNTER = 1


def Option(text: str, scores: List[List[int]], next_states: List[int]=KEEP) -> Dict[str, Any]:
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

def Question(text: str, options: List[Any], title: str=None) -> Dict[str, Any]:
    """
    Make a question with the given text and options
    """
    
    global COUNTER
    
    question = {
        "title": f"Frage {COUNTER}" if title is None else title,
        "text": text,
        "options": options
    }
    
    COUNTER += 1
    
    return question

JSON = {
    "title": "Jagdmodelle",
    "targets": TARGETS,
    "questions": [
        Question(
            "Das ist eine Beispielumfrage. Verstehst du, wie das funktioniert?",
            [
                Option("Fragen und Optionen können dynamisch generiert werden.", [0, 1]),
                Option("Das alles läuft über api.beimgraben.net", [0, 1]),
                Option("Neuerdings sogar mit HTTPS.", [0, 1])
            ],
            title="Oh, wie bist du hier gelandet?!"
        ),
        Question(
            "Als nächstes kommen dann Umfragen, deren Fragen sich live dynamisch generieren. Wie findest du das?",
            [
                Option("Super!", [2, 0]),
                Option("Laaaangweilig", [2, 0]),
                Option("Was mache ich hier nochmal?", [2, 0])
            ],
            title="Immer noch hier? Warum eigentlich?"
        )
    ]
}

# Get base file path and name
base_path = os.path.dirname(__file__)

base_name = os.path.splitext(os.path.basename(__file__))[0]

# Get JSON file name
json_file = os.path.join(base_path, f'{base_name}.json')

# Write JSON to file
with open(json_file, 'w') as f:
    json.dump(JSON, f, indent=4)