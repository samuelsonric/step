from numpy import unique, ndarray, array, vectorize, fromiter
from step.step import leb
from step.terms import Terms
from collections.abc import Sequence


def pullback(step):
    a = unique(step.y)
    return (
        array(tuple(map(step.preimg, a))),
        a,
    )


def normalize(m):
    def inner(x):
        p = m @ x
        if p:
            return x / p
        else:
            return p * x

    return inner


class ConditionalExpectation:
    def __init__(self, E, v):
        self.E = E
        self.v = v

    @classmethod
    def from_pullback(cls, E, pullback):
        return cls(E, array(tuple(map(normalize(E), pullback))))

    def __matmul__(self, other):
        if isinstance(other, Terms):
            return fromiter(map(self.E.__matmul__, self.v * other), dtype="float")
        elif isinstance(other, (ndarray, Sequence)):
            vfun = vectorize(self.E.__matmul__, otypes=("float",))
            return vfun(self.v.reshape(-1, 1) @ other.reshape(1, -1))
        else:
            return NotImplemented
