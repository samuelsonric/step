from step.terms import Terms, TermsAlgebra, terms_of_triples, approx
from step.plotting import plot_step
from numpy import array, fromiter
from itertools import islice, cycle
from bisect import bisect
from math import inf
import matplotlib.pyplot as plt


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
        return cls.from_terms(approx(fun, start, stop, num_steps), y_dtype="float")

    @classmethod
    def from_intervals(cls, intervals, y_dtype=None):
        p = intervals.par
        return cls(
            fromiter(islice(cycle((p, not p)), len(intervals.x)), dtype=y_dtype),
            intervals.x,
        )

    @classmethod
    def one(cls, y_dtype=None):
        return cls.from_triples(((1, -inf, inf),), y_dtype)

    @classmethod
    def zero(cls, y_dtype=None):
        return cls.from_triples(((0, -inf, inf),), y_dtype)

    def iter_terms(self):
        yield from zip(self.y, self.x)

    def plot(self, color="b", xlim=None, ylim=None, figsize=(4, 3)):
        plt.figure(figsize=figsize)
        plot_step(self, color)
        if xlim is not None:
            plt.xlim(*xlim)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.show()

    def __neg__(self):
        return StepFunction(-self.y, self.x)

    def __truediv__(self, other):
        if isinstance(other, Terms):
            raise NotImplementedError
        else:
            return StepFunction(self.y / other, self.x)

    def __mul__(self, other):
        if isinstance(other, Terms):
            return super().__mul__(other)
        elif other:
            return StepFunction(self.y * other, self.x)
        else:
            return StepFunction.zero()

    def __rmul__(self, other):
        return self * other


leb = StepFunction.one(y_dtype="float")
