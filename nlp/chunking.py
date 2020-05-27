# -*- coding: utf-8 -*-

from typing import Callable, Tuple, Any, List, Iterable, Dict
from functional import seq
from functional.pipeline import Sequence
from pathlib import Path
from enum import Enum
from operator import add, itemgetter

import nltk

class NounPhraseChunker():
    """
    Returns lists of tuples like this:
     ('the', 'DT'), ('Brazilian', 'JJ'), ('boa', 'NN'), ('constrictor', 'NN')
    """
    def __init__(self):
        self.grammar = "NP: {<DT>?<JJ>*<NN>}"
        self.cp = nltk.RegexpParser(self.grammar)

    def chunk(self, s: List[Tuple[str, str]]) -> List[str]:
        result = self.cp.parse(s)
        return list(result.subtrees(lambda t: t.label() == "NP"))
