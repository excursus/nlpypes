
from basics import *
from .rules import simple_contractions, contextual_contractions, expansions

class RegexUnion:
    def __init__(self, rules):
        self.rules = rules

    def match(self, s: str):
        return [result for regex, result in self.rules.items()
                       if regex.match(s)]

class Rules:
    def __init__(self):
        self.simple_contractions = RegexUnion(simple_contractions)
        self.contextual_contractions = RegexUnion(contextual_contractions)
        self.expansions = RegexUnion(expansions)
        self.noun_plus_will = re.compile(r"\b\w+'ll\b")

class Contractions:
    def __init__(self, rules=None):
        self.rules = rules or Rules()

    def match(self, s: str,
                    simple=True,
                    contextual=False,
                    expansions=False,     
                    noun_plus_will=False):
        results = []
        if simple:     results.append(self.rules.simple_contractions.match(s))
        if contextual: results.append(self.rules.contextual_contractions.match(s))
        if expansions: results.append(self.rules.expansions.match(s))
        if noun_plus_will: results.append(self.rules.noun_plus_will.match(s))
        return [_ for _ in results if _]

shared = Contractions()