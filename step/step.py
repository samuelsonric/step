from step.terms import TermsAlgebra, terms_of_triples
from numpy import array, tile
from itertools import islice
from bisect import bisect


class StepFunction(TermsAlgebra):
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __call__(self, x):
        return self.y[bisect(self.x, x) - 1]

    @classmethod
    def from_sequences(cls, y, x, y_dtype=None, x_dtype=None):
        return cls(array(y, dtype=y_dtype), array(x, dtype=x_dtype))

    @classmethod
    def from_terms(cls, terms, y_dtype=None, x_dtype=None):
        return cls.from_sequences(*zip(*terms), y_dtype, x_dtype)

    @classmethod
    def from_triples(cls, triples, y_dtype=None, x_dtype=None):
        return cls.from_terms(terms_of_triples(iter(triples)))

    @classmethod
    def from_intervals(cls, intervals, y_dtype='bool'):
        return cls(tile(array((intervals.par, not intervals.par), dtype=y_dtype), len(intervals.x) // 2 + 1), intervals.x)

    @classmethod
    def from_composite(cls, cfun, y_dtype=None):
        return cls(array(tuple(map(cfun.y.__getitem__, cfun.step.y)), dtype=y_dtype), cfun.step.x)

    def iter_terms(self):
        yield from zip(self.y, self.x)

    def __neg__(self):
        return type(self)(-self.y, self.x)
