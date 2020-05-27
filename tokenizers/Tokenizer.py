import nltk
from nltk.tokenize import word_tokenize
from functional import seq
from functional.streams import Sequence
from utils import TextUtils
from typing import Callable, Tuple, Any, List, Iterable
from operator import add
import re
from bs4 import BeautifulSoup

class Tokenizer(object):
    def tokenize(self, s: Any):
        raise Exception("not implemented")

class SentenceTokenizer(Tokenizer):
    def __init__(self):
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def tokenize(self, s: str):
        assert(isinstance(s, str))
        return self.tokenizer.tokenize(s)

class LineTokenizer(Tokenizer):
    def tokenize(self, s: str) -> Sequence:
        s = TextUtils.normalize_newlines(s)
        return seq(re.split(r"\n", s)).filter(TextUtils.has_content)

class DoubleNewlineParagraphTokenizer(Tokenizer):
    def tokenize(self, s: str) -> Sequence:
        s = TextUtils.normalize_newlines(s)
        return seq(re.split(r"\n{2,}", s))

class WordTokenizer(Tokenizer):
    def __init__(self):
        pass
    def tokenize(self, s: str):
        return s.strip().split() # i want to keep apostrophes
        #return word_tokenize(s)

def split(lst: Iterable, cuts: List):
    if len(cuts) == 0:
        yield lst
        return
    if cuts[0] != 0:
        cuts = [0] + cuts
    if cuts[-1] != len(lst):
        cuts = cuts + [len(lst)]

    for left, right in zip(cuts, cuts[1:]):
        yield lst[left:right]

class QuoteParser:
    def parse(self, phrase: str) -> [str]:
        out = []
        for match in re.finditer(r'(“|”|")', phrase):
            mark = match.groups(0)[0]
            if mark == "“":
                out.append(match.start(0))
            if mark == "”":
                out.append(match.end(1))
        return list(split(phrase, out))
