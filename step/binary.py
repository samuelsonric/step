from step.terms import TermsLattice
from itertools import cycle, chain, islice, zip_longest
from bisect import bisect
from math import inf
from numpy import array
from collections import deque


class UnionOfIntervals(TermsLattice):
    repr_pat = "[{1}, {2})"
    repr_sep = " U "

    def __init__(self, par, x):
        self.par = bool(par)
        self.x = x

    def __call__(self, x):
        return self.par == bisect(self.x, x) % 2

    @classmethod
    def from_sequence(cls, par, x, x_dtype=None):
        return cls(par, array(x, dtype=x_dtype))

    @classmethod
    def from_terms(cls, terms, x_dtype=None):
        y, x = zip(*terms)
        return cls.from_sequence(y[0], x, x_dtype)

    @classmethod
    def from_endpoints(cls, endpoints, x_dtype=None):
        x = deque(endpoints)
        if not (par := (x and -inf == x[0])):
            x.appendleft(-inf)
        return cls.from_sequence(par, x, x_dtype)

    @classmethod
    def from_pairs(cls, pairs, x_dtype=None):
        return cls.from_endpoints(chain.from_iterable(pairs), x_dtype)

    @classmethod
    def from_indicator(cls, indicator):
        return cls(indicator.y[0], indicator.x)

    def iter_terms(self):
        c = cycle((self.par, not self.par))
        yield from zip(c, self.x)

    def iter_pairs(self):
        ep = islice(self.x, not self.par, None)
        yield from zip_longest(ep, ep, fillvalue=inf)

    def iter_triples(self):
        def append_true(i):
            return (True, *i)

        yield from map(append_true, self.iter_pairs())

    def __invert__(self):
        return type(self)(not self.par, self.x)

    def __sub__(self, other):
        return self & ~other

    def __xor__(self, other):
        return (self & ~other) | (other & ~self)

    def __eq__(self, other):
        return self.par == other.par and (self.x == other.x).all()
