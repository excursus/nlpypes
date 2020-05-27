from basics import *
from text.unicode import Unicode as U
from nlp.contractions.Contractions import shared as contractions
import re
from enum import Enum

class ApostropheInfo(Enum):
    none = 0
    contraction = 1
    multiple = 2
    other = 3
    noun_plus_will = 4
    apostrophe_s = 5
    ing_apostrophe = 6
    thin_apostrophe = 7

apostrophe_s = re.compile(r"\b\w+'s\b")
ing_apostrophe = re.compile(r"\b\w+in'")
thin_apostrophe = re.compile(r"\b\w+thin'")

# homoglyphs
def categorize(word_: str) -> ApostropheInfo:
    cword = U.APOSTROPHE.make_canonical_in(word_)
    howmany = cword.count(U.APOSTROPHE)

    if howmany == 0:
        return ApostropheInfo.none
    elif howmany >= 2:
        return ApostropheInfo.multiple
    # howmany == 1
    if contractions.match(cword, contextual=True):
        return ApostropheInfo.contraction
    elif contractions.match(cword, simple=False, noun_plus_will=True):
        return ApostropheInfo.noun_plus_will
    elif apostrophe_s.match(cword):
        return ApostropheInfo.apostrophe_s
    elif ing_apostrophe.match(cword):
        return ApostropheInfo.ing_apostrophe
    elif thin_apostrophe.match(cword):
        return ApostropheInfo.thin_apostrophe
    else:
        return ApostropheInfo.other
