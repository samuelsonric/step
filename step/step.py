from step.terms import Terms, TermsAlgebra, terms_of_triples, approx
from numpy import array, fromiter
from itertools import islice, cycle
from bisect import bisect
from math import inf

class StepFunction(TermsAlgebra):
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __call__(self, x):
        return self.y[bisect(self.x, x) - 1]

    @classmethod
    def from_sequences(cls, y, x, y_dtype=None):
        return cls(array(y, dtype=y_dtype), array(x))

    @classmethod
    def from_terms(cls, terms, y_dtype=None):
        return cls.from_sequences(*zip(*terms), y_dtype)

    @classmethod
    def from_triples(cls, triples, y_dtype=None):
        return cls.from_terms(terms_of_triples(iter(triples)), y_dtype)

    @classmethod
    def approx(cls, fun, start, stop, num_steps=100):
        return cls.from_terms(approx(fun, start, stop, num_steps), y_dtype='float')


    @classmethod
    def from_intervals(cls, intervals, y_dtype='bool'):
        p = intervals.par
        return cls(
            fromiter(islice(cycle((p, not p)), len(intervals.x)), dtype=y_dtype),
            intervals.x
        )

    def iter_terms(self):
        yield from zip(self.y, self.x)

    def __neg__(self):
        return type(self)(-self.y, self.x)

    def __mul__(self, other):
        if isinstance(other, Terms):
            return super().__mul__(other)
        else:
            return type(self)(other * self.y, self.x)

    def __rmul__(self, other):
        return self * other

leb = StepFunction.from_triples(((True, -inf, inf),))
