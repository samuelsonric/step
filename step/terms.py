from math import inf
from itertools import zip_longest
from numpy import linspace, array
from operator import mul, neg, add, sub, not_, truth


def equal(x, y):
    return all(i == j for i, j in zip_longest(x, y))


def call(val, x):
    def filt(i):
        return i[1] <= val < i[2]

    return next(filter(filt, triples_of_terms(x)))


def triples_of_terms(x):
    filt = lambda x: x[0]
    yield from filter(filt, triples_of_terms0(x))


def triples_of_terms0(x):
    i = next(x)
    for j in x:
        yield (*i, j[1])
        i = j
    yield (*i, inf)


def terms_of_triple(i):
    yield (i[0], i[1])
    if i[2] < inf:
        yield (0, i[2])


def terms_of_triples(x):
    i = next(x, (0, -inf, inf))
    yield from terms_of_triple(i)
    yield from map(terms_of_triple, x)


def leb_of_triple(i):
    return i[0] and i[0] * (i[2] - i[1])


def leb(x):
    return sum(map(leb_of_triple, triples_of_terms(x)))


def reduce_terms(x):
    p = None
    for i in x:
        if not p == i[0]:
            p = i[0]
            yield i


def pointwise_binary(op, x, y):
    yield from reduce_terms(pointwise_binary_0(op, x, y))


def pointwise_unary(op, x):
    yield from reduce_terms(pointwise_unary_0(op, x))


def approx(fun, start, stop, num_steps):
    yield from reduce_terms(approx_0(fun, start, stop, num_steps))


def pointwise_binary_0(op, x, y):
    i = next(x)
    j = next(y)
    sentinel = (0, inf)

    while not i == j == sentinel:
        if i[1] < j[1]:
            yield (op(i[0], jh[0]), i[1])
            ih = i
            i = next(x, sentinel)
        elif j[1] < i[1]:
            yield (op(ih[0], j[0]), j[1])
            jh = j
            j = next(y, sentinel)
        else:
            yield (op(i[0], j[0]), i[1])
            ih = i
            jh = j
            i = next(x, sentinel)
            j = next(y, sentinel)


def pointwise_unary_0(op, x):
    for i in x:
        yield (op(i[0]), i[1])


def graph_of_fun(fun):
    return lambda x: (fun(x), x)


def approx_0(fun, start, stop, num_steps):
    yield (0, -inf)
    yield from map(graph_of_fun(fun), linspace(start, stop, num_steps, endpoint=False))
    yield (0, stop)


class Terms:
    repr_pat = "{}[{}, {})"
    repr_sep = " + "
    repr_num = 3

    @classmethod
    def from_terms(cls, terms):
        raise NotImplementedError

    @classmethod
    def from_triples(cls, triples):
        return cls.from_terms(terms_of_triples(iter(triples)))

    @classmethod
    def from_function(cls, fun, start=-10, stop=10, num_steps=100):
        return self.from_terms(approx(fun, start, stop, num_steps))

    def iter_terms(self):
        raise NotImplementedError

    def iter_triples(self):
        yield from triples_of_terms(self.iter_terms())

    def leb(self):
        return leb(self.iter_terms())

    def __matmul__(self, other):
        return leb(pointwise_binary(mul, self.iter_terms(), other.iter_terms()))

    def __call__(self, x):
        call(x, self.iter_terms())

    def __eq__(self, other):
        return equal(self.iter_terms(), other.iter_terms())

    def __repr__(self):
        l = []
        for n, i in enumerate(self.iter_triples()):
            if n < self.repr_num:
                l.append(self.repr_pat.format(*i))
            else:
                l.append("...")
                break
        return f"{type(self).__name__}({self.repr_sep.join(l)})"


class TermsLattice(Terms):
    def __and__(self, other):
        return self.from_terms(
            pointwise_binary(min, self.iter_terms(), other.iter_terms())
        )

    def __or__(self, other):
        return self.from_terms(
            pointwise_binary(max, self.iter_terms(), other.iter_terms())
        )

    def __le__(self, other):
        return self == self & other

    def __lt__(self, other):
        return self <= other and not self == other


class TermsAlgebra(TermsLattice):
    def __neg__(self, other):
        return self.from_terms(pointwise_unary(neg, self.iter_terms()))

    def __add__(self, other):
        return self.from_terms(
            pointwise_binary(add, self.iter_terms(), other.iter_terms())
        )

    def __sub__(self, other):
        return self.from_terms(
            pointwise_binary(sub, self.iter_terms(), other.iter_terms())
        )

    def __mul__(self, other):
        return self.from_terms(
            pointwise_binary(mul, self.iter_terms(), other.iter_terms())
        )

    def __floordiv__(self, other):
        def div(x, y):
            return y and x / y

        return self.from_terms(
            pointwise_binary(div, self.iter_terms(), other.iter_terms())
        )

    def __mod__(self, other):
        # return self - ((self // other) * other)
        # return self * (self.supp() * other.ker())
        return self.from_terms(
            pointwise_binary(
                mul,
                self.iter_terms(),
                pointwise_binary(
                    mul,
                    pointwise_unary(truth, self.iter_terms()),
                    pointwise_unary(not_, other.iter_terms()),
                ),
            )
        )

    def __abs__(self):
        return self.from_terms(pointwise_unary(abs, self.iter_terms()))

    def ppart(self):
        return self.from_terms(
            pointwise_unary(lambda x: x > 0 and x, self.iter_terms())
        )

    def npart(self):
        return self.from_terms(
            pointwise_unary(lambda x: x < 0 and x, self.iter_terms())
        )

    def supp(self):
        return self.from_terms(pointwise_unary(truth, self.iter_terms()))

    def ker(self):
        return self.from_terms(pointwise_unary(not_, self.iter_terms()))

    def pset(self):
        return self.from_terms(pointwise_unary(lambda x: x > 0, self.iter_terms()))

    def nset(self):
        return self.from_terms(pointwise_unary(lambda x: x < 0, self.iter_terms()))
