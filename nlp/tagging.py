# -*- coding: utf-8 -*-

from typing import Callable, Tuple, Any, List, Iterable, Dict
from functional import seq
from functional.pipeline import Sequence
from pathlib import Path
from enum import Enum
import nltk
from operator import itemgetter

class POSTaggedList(list):
    """This will have format
    [('Not', 'RB'), ('for', 'IN'), ('the', 'DT'), ('first', 'JJ'), ...]
    """
    def flatten(self) -> list:
        return list(map(itemgetter(0), self))


class POSTagger():
    def tag(self, x: List[str]) -> POSTaggedList:
        assert(isinstance(x, list))        
        return POSTaggedList(nltk.pos_tag(x))


