from collections.abc import Iterable
import re
from functional.pipeline import Sequence
from functional import seq
from polyglot.text import Word
from enum import Enum
from typing import Callable


class Numbers:
    units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"]

    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    regex_str = r'(\d+|%s)' % ("|".join(units + tens))

class TextFeatures(Enum):
    def __init__(self, val):
        super().__init__()
    parens = 1
    brackets = 2
    curly_braces = 3


class TextUtils:
    class Regex:
        heading = re.compile(r'^\s*chapter\s*%s+\s*' % Numbers.regex_str, re.IGNORECASE)
        remove_two = lambda left, right: re.compile("%s.*?%s" % (left, right))
        isnontext = re.compile(r'^[^a-zA-z]*$')

    @staticmethod
    def normalize_newlines(s: str) -> str:
        return re.sub(r"(\r\n)", "\n", s)

    @staticmethod
    def isHeading(s: str) -> bool:
        return re.match(TextUtils.Regex.heading, s) is not None
    def isNotHeading(s: str) -> bool:
        return not TextUtils.isHeading(s)

    @staticmethod
    def has_content(s: str) -> bool:
        return len(s.strip()) > 0

    @staticmethod
    def isText(s: str) -> bool:
        return not TextUtils.isNontext(s)

    @staticmethod
    def isNontext(s: str) -> bool:
        return re.match(TextUtils.Regex.isnontext, s)

    @staticmethod
    def removeSpanning(target: str, left: str, right: str):
        assert(isinstance(target, str) and isinstance(left, str) and isinstance(right, str))
        regex = TextUtils.Regex.remove_two(left, right)
        return regex.sub("", target)

# class String(str):
#     wt = WordTokenizer()

#     @property
#     def words(self):
#         return String.wt.tokenize(self)

#     def contains(self, needle):
#         return needle in self

#     def morphemes(self):
#         w = Word(self, language="en")
#         return w.morphemes

#     def remove(self, what: TextFeatures):
# #        print(what, TextFeatures, type(what), id(type(what)), id(TextFeatures))
#         assert(isinstance(what, TextFeatures))
#         m = {TextFeatures.parens: (r'\(', r'\)'),
#                 TextFeatures.brackets: (r'\[',r'\]'),
#                 TextFeatures.curly_braces: (r'\{', r'\}')}
#         args = m[what]
#         return String(TextUtils.removeSpanning(self, *args))

def grep(s_list, window=3):
    if type(s_list) == str:
        return grep(s_list.split())


def window(s: Sequence, n: int):
    def helper(s: Sequence, n: int):
        assert(isinstance(s, Sequence) and isinstance(n, int))
        acc = []
        for elem in s:
            if len(acc) < n:
                acc += [elem]
            elif len(acc) == n:
                yield acc
                acc = acc[1:] + [elem]
    return seq(helper(s, n))


class WordBag:
    pass

class WordSet(WordBag, set):
    pass

class Graph:
    pass

class Thesaurus(WordSet, Graph):
    pass
