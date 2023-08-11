#!/usr/bin/env python3
"""
Survey loading and parsing

Survey templates are saves as a JSON file like this:
```json
{
    "targets": [
        {
            "name": "Target 1",
            "states": 2
        },
        {
            "name": "Target 2",
            "states": 1
        },
        ...
    ],
    "questions": [
        {
            "title": "Example Question",
            "text": "This is an example question",
            "options": [
                {
                    "text": "Option 1",
                    "scores": [
                        [0, 3],
                        [1],
                        ...
                    ],
                    "next_state": [1, 0, ...]
                },
                {
                    "text": "Option 2",
                    "scores": [
                        [0, 1],
                        [1],
                        ...
                    ],
                    "next_states": [1, 0, ...]
                },
                ...
            ]
        },
        ...
    ]
}
```

This module loads the JSON file and parses it into a list of Question objects.
These can be converted into a "UI-Only" JSON format for the frontend to use.
Also it can be fed the JSON returned from the frontend to calculate their results.
"""

import json
import os
import flask

from typing import Dict, List, Any, Generator, Tuple, Union

JSONPrimitives = Any # str | int | float | bool | None

JSON = Any
# Dict[
#    str,
#    'JSON'
# ] | List['JSON'] | JSONPrimitives

class SurveyError(Exception):
    """Base class for all survey errors"""
    
    pass

class Target:
    name: str
    n_states: int
    
    def __init__(self, json: JSON):
        self.name = json["name"]
        self.n_states = json["states"]
        
    def to_json(self):
        return {
            "name": self.name,
            "states": self.n_states
        }
        
    def __repr__(self):
        return f"Target({self.to_json()})"
        
class TargetState:
    target: Target
    state: int
    
    @property
    def n_states(self):
        return self.target.n_states
    
    @property
    def name(self):
        return self.target.name
    
    def __init__(self, target: Target, state: int):
        self.target = target
        self.state = state
        
    def to_json(self):
        return {
            "target": self.target.name,
            "state": self.state
        }
        
    def set_state(self, state: int) -> int:
        if not -1 <= state < self.n_states:
            raise SurveyError("Invalid state")
        
        old_state = self.state
        
        if state != -1:
            self.state = state
            
        return old_state
            
    def __repr__(self):
        return f"TargetState({self.target}, {self.state})"

TargetStatePair = Tuple[int, TargetState]
TargetStates = List[TargetStatePair]
Targets = List[Target]

class Option:
    text: str
    scores: List[List[int]]
    next_states: List[int]
    
    def __init__(self, json: dict, targets: List[Target]):
        self.text = json["text"]
        
        scores_raw = json["scores"]
        
        scores = []
        
        # If scores are one-dimensional, copy them for every target
        for score, target in zip(scores_raw, targets):
            if not isinstance(score, list):
                scores.append([score] * target.n_states)
            else:
                scores.append(score)
                
        self.scores = scores
        
        self.next_states = json["next_states"]
        
        for next_state, target in zip(self.next_states, targets):
            if not -1 <= next_state < target.n_states:
                raise SurveyError("Invalid next state")
        
    def to_json(self) -> JSON:
        return {
            "text": self.text,
            "scores": self.scores
        }
        
    def eval(self, targets: TargetStates) -> Generator[int, None, None]:
        """Evaluate the option for the given targets"""

        if not len(targets) == len(self.scores):
            raise SurveyError("Number of targets does not match number of scores")

        for (i, target), score in zip(targets, self.scores):
            if not 0 <= i < len(self.scores):
                raise SurveyError(f"Invalid target index: {i}/{len(self.scores)}")
            
            yield score[target.set_state(self.next_states[i])]
            
    def to_frontend(self, targets: TargetStates) -> JSON:
        """Convert the option to a JSON object for the frontend"""
        
        return self.text


class Question:
    title: str
    text: str
    options: List[Option]
    
    def __init__(self, json: dict, targets: Targets):
        self.title = json["title"]
        self.text = json["text"]
        self.options = [Option(o, targets) for o in json["options"]]
        
    def to_json(self) -> JSON:
        return {
            "title": self.title,
            "text": self.text,
            "options": [o.to_json() for o in self.options]
        }
        
    def eval(self, option: int, targets: TargetStates) -> Generator[int, None, None]:
        """Evaluate the question for the given targets and option"""
        
        if not 0 <= option < len(self.options):
            raise SurveyError("Invalid option")
            
        yield from self.options[option].eval(targets)
        
    def __repr__(self) -> str:
        return f"Question({self.to_json()})"
        
    def to_frontend(self, targets: TargetStates) -> JSON:
        """Convert the question to a JSON object for the frontend"""
        
        return {
            "title": self.title,
            "text": self.text,
            "options": [o.to_frontend(targets) for o in self.options]
        }   

INSTANCES = {}

def radio_page(id: str, title: str, text: str, options: List[JSON]) -> JSON:
    """Create a radio page for the frontend"""
    
    return {
        "name": id,
        "title": title,
        "elements": [
            {
                "type": "radiogroup",
                "name": id + "_radio",
                "title": text,
                "isRequired": True,
                "valueName": id,
                "clearIfInvisible": "none",
                "choices": options
            }
        ]
    }
    
def question_to_page(id: str, question: Question) -> JSON:
    """Convert a question to a page for the frontend"""
    
    return radio_page(
        id=id,
        title=question.title,
        text=question.text,
        options=[
            o.text for o in question.options
        ]
    )

class Survey:
    title: str
    targets: List[Target]
    questions: List[Question]
    
    def __init__(self, json: dict):
        self.title = json["title"]
        self.targets = [Target(t) for t in json["targets"]]
        self.questions = [Question(q, self.targets) for q in json["questions"]]
        
    def to_json(self) -> JSON:
        return {
            "targets": [t.to_json() for t in self.targets],
            "questions": [q.to_json() for q in self.questions]
        }
        
    def __eval(self, answers: List[int], targets: TargetStates) -> Generator[Generator[int, None, None], None, None]:
        """Evaluate the survey for the given answers"""
        
        if not len(answers) == len(self.questions):
            raise SurveyError("Number of answers does not match number of questions")
            
        for question, answer in zip(self.questions, answers):
            yield question.eval(answer, targets)
        
    def eval(self, answers: List[int]) -> List[Dict]:
        """
        Evaluate the survey for the given answers
        
        Return the sums for each Target
        """
        
        targets = [(i, TargetState(t, 0)) for i, t in enumerate(self.targets)]
        
        results = list(map(sum, zip(*self.__eval(answers, targets))))
        
        if sum(results) == 0:
            results = [1] * len(results)
        
        percents = list(map(lambda x: x / sum(results), results))
        
        targets_o = [target for _, target in targets]
        
        result = [
            {
                "target": t.name,
                "end_state": t.state,
                "percent": p,
                "winner": p == max(percents) and (p > 0.5 or i == 0),
                "result": r
            } for i, (t, p, r) in enumerate(zip(targets_o, percents, results))
        ]
        
        return result
        
    def __repr__(self) -> str:
        return f"Survey({self.to_json()})"
    
    def to_frontend(self) -> JSON:
        """Convert the survey to a JSON object for the frontend"""
        
        # [q.to_frontend([(i, t) for i, t in enumerate(self.targets)]) for q in self.questions]
        
        return {
            "title": self.title,
            "checkErrorsMode": "onValueChanged",
            "pages": [
                question_to_page(str(i), q) for i, q in enumerate(self.questions)
            ]
        }

def load_survey(path: str) -> Survey:
    """Load a survey from a JSON file"""
    
    with open(path) as f:
        return Survey(json.load(f))