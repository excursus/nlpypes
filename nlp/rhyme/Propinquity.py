from basics import *

class Propinquity:
    def __call__(self, lhs, rhs) -> float:
        raise NotImplementedError()

    def __add__(self, num):
        return PropinquityAddition(self, num)
    def __radd__(self, num):
        return PropinquityAddition(self, num)
    def __mul__(self, num):
        return PropinquityMultiplication(self, num)
    def __rmul__(self, num):
        return PropinquityMultiplication(self, num)
    def to(self, first):
        """ Binds the first argument, producing a unary operator """
        def inner(second):
            return self(first, second)
        return inner

    def _matches(self, lhs: list, rhs: list, func):
        matches = func(lhs, rhs)
        num_matches = len(list(takewhile(identity, reversed(matches))))
        lhs_len, rhs_len = len(lhs), len(rhs)

        if num_matches == 0:
            return 0
        elif lhs_len == rhs_len == num_matches:
            return 0
        else:
            return num_matches

class PropinquityAddition(Propinquity):
    def __init__(self, inner, base):
        self.inner = inner
        self.base = base

    def __call__(self, lhs, rhs):
        return self.inner() + self.base


class PropinquityMultiplication(Propinquity):
    def __init__(self, inner, multiplier):
        self.inner = inner
        self.multiplier = multiplier

    def __call__(self, lhs, rhs):
        return self.inner() * self.multiplier
