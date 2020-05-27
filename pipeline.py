from enum import Enum
from fn import _
from functional import seq
from functional.streams import Sequence
from pathlib import Path
from typing import List, Tuple, Any, Callable, Iterable
from utils import TextUtils, TextFeatures
import re
from io import TextIOWrapper
from tqdm import tqdm

class Op(Enum):
    map = 1
    reduce = 2
    filter = 3
    flat_map = 4
    chunk = 5
    nonsequential = 6

class Pipeline:
    def __init__(self, transforms: List[Tuple[Op, Any]]):
        assert(list(map(len, transforms)) == [2] * len(transforms))
        self.transforms = transforms

    def readfrom(self, path: Path):
        lines = seq(path.open().readlines())
        return self.run(lines)

    def run(self, stream_: Sequence) -> Sequence:
        assert(isinstance(stream_, Sequence))
        stream = seq(stream_)
        for (op, transform) in self.transforms:
            if op == Op.map:
                stream = stream.map(transform)
            elif op == Op.filter:
                stream = stream.filter(transform)
            elif op == Op.reduce:
                stream = stream.reduce(transform)
            elif op == Op.flat_map:
                stream = stream.flat_map(transform)
            elif op == Op.chunk:
                assert(len(transform) == 2)
                stream = stream.chunk(*transform)
            elif op == Op.nonsequential:
                s: str = " ".join(list(stream))
                stream = seq(transform(s))
            else:
                raise Exception()
        return stream

    ## Pipelines are composible using the `>` operator.
    def __or__(self, other):
        if isinstance(other, Pipeline):
            return Pipeline(self.transforms + other.transforms)
        elif isinstance(other, tuple) and len(other) == 2:
            return Pipeline(self.transforms + [other])
        else:
            raise ValueError(f"Unsupported parameter type {type(other)}")

    ## Pipeline generators
    @staticmethod
    def filter(x: Callable[[str], bool]) -> "Pipeline":
        return P([(Op.filter, x)])

    @staticmethod
    def containing(x: Any) -> "Pipeline":
        return P([(Op.filter, lambda s: x in s)])

    @staticmethod
    def flat_map(func: Callable) -> "Pipeline":
        return P([(Op.flat_map, func)])

    @staticmethod
    def map(func: Callable) -> "Pipeline":
        return P([(Op.map, func)])

    @staticmethod
    def identity():
        return P.map(lambda x: x)

    @staticmethod
    def spy(func):
        def inner(x):
            func(x)
            return x
        return P.map(inner)


## Adding convenience static properties to the `Pipeline` class:
P = Pipeline
P.default = P([(Op.map, str.strip), (Op.filter, TextUtils.isText)])
P.lowercase = P([(Op.map, lambda x: x.lower())])
P.wrangled = P.default | P.filter(TextUtils.isText) | P.filter(TextUtils.isNotHeading)
P.wrap = P([(Op.map, lambda x: "[%s]" % x)])
P.newlines = P([(Op.map, lambda x: f"\n{x}")])
P.prefix = lambda f: P([(Op.map, lambda s: f'::{f(s)}:: {s}')])
P.noParens = Pipeline([(Op.map, lambda x: x.remove(TextFeatures.parens))])
P.noBrackets = Pipeline([(Op.map, lambda x: x.remove(TextFeatures.brackets))])
P.noCurlyBraces = Pipeline([(Op.map, lambda x: x.remove(TextFeatures.curly_braces))])

def pprint(s, maxlines=10):
    """Pretty print for sequences"""
    if isinstance(s, str):
        pprint(s.split())
    elif isinstance(s, Sequence):
        s = s.take(maxlines)
    elif isinstance(s, Iterable):
        s = s[:maxlines]
    else:
        raise Exception
    for e in s:
        print(e)

def Sequence__or__(self, other) -> Sequence:
    """A shim to get PyFunctional's sequences to support the | operator."""
    if isinstance(other, Pipeline):
        return other.run(self)
    elif isinstance(other, TextIOWrapper):
        for e in self:
            other.write(e)
            other.write("\n")
    elif other is pprint:
        pprint(self)
Sequence.__or__ = Sequence__or__
