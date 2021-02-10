from step.terms import Algebra, Lep, compress
from numpy import array, fromiter, dtype, unique
from itertools import islice, cycle
from bisect import bisect
from math import inf
import matplotlib.pyplot as plt


class StepFunction(Algebra):
    def __init__(self, y0, y, x, cl):
        self.y0 = y0
        self.y = y
        self.x = x
        self.cl = cl

    def __len__(self):
        return len(self.x)

    def __call__(self, a):
        if self and self.x[0] < a:
            i = bisect(self.x, a) - 1
            if self.x[i] == a and not self.cl[i]:
                i -= 1
            return self.y[i]
        elif self and self.x[0] == a and self.cl[0]:
            return self.y[0]
        else:
            return self.y0

    @classmethod
    def from_sequences(cls, y0, y, x, cl, y_dtype=None, x_dtype=None):
        return cls(
            y0 = dtype(y_dtype).type(y0),
            y = array(y, dtype=y_dtype),
            x = array(x, dtype=x_dtype),
            cl = array(cl),
        )

    @classmethod
    def from_compressed_lep(cls, lep, y_dtype=None, x_dtype=None):
        y, x, cl = zip(*lep)
        return cls.from_sequences(y[0], y[1:], x[1:], cl[1:], y_dtype, x_dtype)

    @classmethod
    def from_lep(cls, lep, y_dtype=None, x_dtype=None):
        return cls.from_compressed_lep(compress(iter(lep)), y_dtype, x_dtype)

    @classmethod
    def one(cls, y_dtype=None):
        return cls.from_lep(((1, -inf, False),), y_dtype)

    @classmethod
    def zero(cls, y_dtype=None):
        return cls.from_lep(((0, -inf, False),), y_dtype)

    def iter_lep(self):
        yield (self.y0, -inf, False)
        yield from zip(self.y, self.x, self.cl)

    def __neg__(self):
        return StepFunction(-self.y0, -self.y, self.x, self.cl)

    def __truediv__(self, other):
        if isinstance(other, Lep):
            raise NotImplementedError
        else:
            return type(self)(self.y0 / other, self.y / other, self.x, self.cl)

    def __mul__(self, other):
        if isinstance(other, Lep):
            return super().__mul__(other)
        elif other:
            return type(self)(self.y0 * other, self.y * other, self.x, self.cl)
        else:
            return type(self).zero()

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        if isinstance(other, CompositionOperator):
            return CompositionOperator(
                preimg = fromiter(map(self.__matmul__, other.preimg), dtype='float', count=len(other.preimg)),
                y = other.y,
            )
        else:
            return super().__matmul__(other)

class CompositionOperator:
    def __init__(self, preimg, y):
        self.preimg = preimg
        self.y = y

    @classmethod
    def from_step(cls, step):
        a = unique((step.y0, *step.y))
        return cls(array(tuple(map(step.preimg, a))), a)

    def __matmul__(self, other):
        return self.preimg @ fromiter(map(other.__call__, self.y), dtype='float', count=len(self.y))


leb = StepFunction.one(y_dtype='float')
