from . import Tokenizer
from typing import Any, Dict
from corpus.DiscourseUnit import DiscourseUnit

class TokenizerFactory():
    def __init__(self, t_map: Dict[DiscourseUnit, Any]={}):
        self.t_map = t_map

    def get(self, obj: Any) -> Tokenizer:
        if isinstance(obj, DiscourseUnit):
            return self.t_map.get(obj, None)
        raise NotImplementedError()
