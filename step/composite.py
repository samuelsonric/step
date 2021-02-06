from step.terms import Terms
from step.step import StepFunction
from numpy import maximum, minimum, array, fromiter, float64
from collections import OrderedDict


class CompositeFunction(Terms):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, x):
        return self.left[self.right(x)]

    @classmethod
    def from_terms(cls, terms):
        left = OrderedDict()
        right = []
        for i in terms:
            right.append((left.setdefault(i[0], len(left)), i[1]))
        return cls(fromiter(left, float64), StepFunction.from_array(right))

    @classmethod
    def from_step(cls, step):
        return cls.from_terms(step.iter_terms())

    @classmethod
    def from_intervals(cls, intervals):
        return cls(array((1, 0)), StepFunction.from_terms(intervals.iter_terms()))

    def iter_terms(self):
        for i in self.right.iter_terms():
            yield (self.left[int(i[0])], i[1])

    def __neg__(self):
        return type(self)(-self.left, self.right)

    def __add__(self, other):
        return type(self)(self.left + other.left, self.right)

    def __sub__(self, other):
        return type(self)(self.left - other.left, self.right)

    def __mul__(self, other):
        return type(self)(self.left * other.left, self.right)

    def __or__(self, other):
        return type(self)(maximum(self.left, other.left), self.right)

    def __and__(self, other):
        return type(self)(minimum(self.left, other.left), self.right)

    def __eq__(self, other):
        return (self.left == other.left).all()

    def __le__(self, other):
        return (self.left <= other.left).all()

    def __lt__(self, other):
        return (self.left < other.left).all()
