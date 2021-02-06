from step.terms import TermsAlgebra
from numpy import array
from itertools import islice
from bisect import bisect


class StepFunction(TermsAlgebra):
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __call__(self, x):
        return self.y[bisect(self.x, x) - 1]

    @classmethod
    def from_sequences(cls, y, x):
        return cls(array(y), array(x))

    @classmethod
    def from_terms(cls, terms):
        return cls.from_sequences(*zip(*terms))

    @classmethod
    def from_intervals(cls, intervals):
        return cls.from_terms(intervals.iter_terms())

    @classmethod
    def from_composite(cls, cfun):
        return cls.from_terms(cfun.iter_terms())

    def iter_terms(self):
        yield from zip(self.y, self.x)

    def __neg__(self):
        return type(self)(-self.y, self.x)
