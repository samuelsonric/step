from step.terms import TermsLattice, TermsVectorSpace
from numpy import array
from itertools import islice
from bisect import bisect


class StepFunction(TermsLattice, TermsVectorSpace):
    def __init__(self, mat):
        self.mat = mat

    def __call__(self, x):
        return self.mat[bisect(self.mat[:, 1], x) - 1, 0]

    @classmethod
    def from_array(cls, arr):
        return cls(array(arr))

    @classmethod
    def from_terms(cls, terms):
        return cls.from_array(tuple(terms))

    @classmethod
    def from_intervals(cls, intervals):
        return cls.from_terms(intervals.iter_terms())

    @classmethod
    def from_composite(cls, cfun):
        return cls.from_terms(cfun.iter_terms())

    def iter_terms(self):
        yield from map(tuple, self.mat)

    def __neg__(self):
        return type(self)(self.mat * (-1, 0))
