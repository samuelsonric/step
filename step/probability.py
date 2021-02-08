from step.terms import reduce_terms
from step.step import StepFunction
from numpy import unique, array, vectorize, ndarray
from functools import cached_property
from math import inf
from collections.abc import Sequence


def pullback(step):
    a = unique(step.y)
    return (
        array(tuple(map(step.preimg, a))),
        a,
    )

def conditional_distr(m, x, y):
    a = vectorize(m.__matmul__, otypes=("float",))(x.reshape(-1, 1) @ y.reshape(1, -1))
    s = a.sum(axis=1).reshape(-1, 1)
    s[s == 0] = 1
    return a / s


