from math import inf
from itertools import zip_longest, chain
from numpy import linspace
from operator import add
from functools import wraps


# coor: (y, x, cl)

def compress(x):
    p = None
    for i in x:
        if not p == i[0]:
            p = i[0]
            yield i


def binary_op(op, x, y):
    i = next(x)
    j = next(y)
    sentinel = (0, inf, False)

    while not i == j == sentinel:
        if i[1] < j[1] or (i[1] == j[1] and i[2] > j[2]):
            yield (op(i[0], jh[0]), *i[1:])
            ih = i
            i = next(x, sentinel)
        elif j[1] < i[1] or (j[1] == i[1] and j[2] > i[2]):
            yield (op(ih[0], j[0]), *j[1:])
            jh = j
            j = next(y, sentinel)
        else:
            yield (op(i[0], j[0]), *i[1:])
            ih = i
            jh = j
            i = next(x, sentinel)
            j = next(y, sentinel)


def unary_op(op, x):
    for i in x:
        yield (op(i[0]), *i[1:])


class Lep:
    @classmethod
    def from_compressed_lep(cls, lep):
        raise NotImplementedError

    @classmethod
    def from_lep(cls, lep):
        return cls.from_compressed_lep(compress(iter(lep)))

    def iter_lep(self):
        raise NotImplementedError

    def __eq__(self, other):
        return all(i == j for i, j in zip_longest(x.iter_lep(), y.iter_lep()))

def binary(op):
    @wraps(op)
    def inner(self, other):
        return self.from_lep(binary_op(op, self.iter_lep(), other.iter_lep()))

    return inner


def unary(op):
    @wraps(op)
    def inner(self):
        return self.from_lep(unary_op(op, self.iter_lep()))

    return inner


def scalar(op):
    @wraps(op)
    def inner(self, a):
        return self.from_lep(unary_op(lambda x: op(x, a), self.iter_lep()))

    return inner


class Lattice(Lep):
    @binary
    def __and__(self, other):
        return min(self, other)

    @binary
    def __or__(self, other):
        return max(self, other)

    def __le__(self, other):
        return self == self & other

    def __lt__(self, other):
        return self <= other and not self == other


def rect(x):
    i = next(x)
    for j in x:
        yield i[0] and i[0] * (j[1] - i[1])
        i = j
    yield i[0] and i[0] * inf
    

def graph_of_fun(fun):
    return lambda x: (fun(x), x, True)


def approx(fun, start, stop, num_steps):
    yield (0, -inf, False)
    yield from map(graph_of_fun(fun), linspace(start, stop, num_steps, endpoint=False))
    yield (0, stop, True)


class Algebra(Lattice):
    @classmethod
    def approx(cls, fun, start, stop, num_steps=100):
        return cls.from_terms(approx(fun, start, stop, num_steps))

    def __matmul__(self, other):
        if isinstance(other, Lep):
            p = self * other
            return sum(rect(p.iter_lep()))
        else:
            return NotImplemented

    @unary
    def __neg__(x):
        return -x

    @binary
    def __add__(x, y):
        return x + y

    @binary
    def __sub__(x, y):
        return x - y

    @binary
    def __mul__(x, y):
        return x * y

    @binary
    def __floordiv__(x, y):
        return y and x / y

    @binary
    def __mod__(x, y):
        return y == 0 and x

    @unary
    def __abs__(x):
        return abs(x)

    @scalar
    def __pow__(x, n):
        return x ** n

    @unary
    def ppart(x):
        return x > 0 and x

    @unary
    def npart(x):
        return x < 0 and x

    @scalar
    def preimg(x, a):
        return x == a

    @unary
    def supp(x):
        return truth(x)

    @unary
    def ker(x):
        return not x

    @unary
    def pset(x):
        return x > 0

    @unary
    def nset(x):
        return x < 0

    def __lshift__(self, other):
        return self.supp() <= other.supp()

    def __rshift__(self, other):
        return self.supp() >= other.supp()
