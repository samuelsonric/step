from step.terms import TermsLattice
from itertools import cycle, chain, islice, zip_longest
from bisect import bisect
from math import inf
from numpy import array
from collections import deque


class UnionOfIntervals(TermsLattice):
    repr_pat = "[{1}, {2})"
    repr_sep = " U "

    def __init__(self, parity, endpoints):
        self.parity = parity
        self.endpoints = endpoints

    def __call__(self, x):
        return self.parity == bisect(self.endpoints, x) % 2

    @classmethod
    def from_terms(cls, terms):
        coef, ep = zip(*terms)
        return cls(coef[0], array(ep))

    @classmethod
    def from_indicator(cls, indicator):
        return cls.from_terms(indicator.iter_terms())

    @classmethod
    def from_endpoints(cls, endpoints):
        ep = deque(endpoints)
        if not (p := (ep and -inf == ep[0])):
            ep.appendleft(-inf)
        return cls(p, array(ep))

    @classmethod
    def from_pairs(cls, pairs):
        return cls.from_endpoints(chain.from_iterable(pairs))

    def iter_terms(self):
        c = cycle((self.parity, not self.parity))
        yield from zip(c, self.endpoints)

    def iter_pairs(self):
        ep = islice(self.endpoints, not self.parity, None)
        yield from zip_longest(ep, ep, fillvalue=inf)

    def iter_triples(self):
        def append_true(i):
            return (True, *i)

        yield from map(append_true, self.iter_pairs())

    def __invert__(self):
        return type(self)(not self.parity, self.endpoints)

    def __sub__(self, other):
        return self & ~other

    def __xor__(self, other):
        return (self & ~other) | (other & ~self)

    def __eq__(self, other):
        return self.parity == other.parity and (self.endpoints == other.endpoints).all()
