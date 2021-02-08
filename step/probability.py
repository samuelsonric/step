from step.terms import reduce_terms
from step.step import StepFunction
from numpy import unique, array, vectorize
from functools import cached_property
from math import inf


class Pullback:
    def __init__(self, vec):
        self.vec = vec

    @classmethod
    def from_step(cls, step):
        return cls(pullback_0(step)[0])

    def __matmul__(self, other):
        if other.ndim > 1:
            return Pullback(self.vec @ other)
        else:
            return self.vec @ other

    # TODO
    def __mul__(self, other):
        raise NotImplementedError


def pullback_0(step):
    a = unique(step.y)
    return (
        array(tuple(map(step.preimg, a))),
        a,
    )


def pullback(step):
    vec, a = pull_back_0(step)
    return (Pullback(vec), a)


def conditional_distr_0(m, x, y):
    a = vectorize(m.__matmul__, otypes=("float",))(x.reshape(-1, 1) @ y.reshape(1, -1))
    s = a.sum(axis=1).reshape(-1, 1)
    s[s == 0] = 1
    return a / s


def conditional_distr(m, x, y):
    return conditional_distr_0(m, x.vec, y.vec)
