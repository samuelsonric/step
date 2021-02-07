from step.terms import Terms
from step.step import StepFunction
from numpy import maximum, minimum, array
from collections import OrderedDict


class CompositeFunction(Terms):
    def __init__(self, y, step):
        self.y = y
        self.step = step

    def __call__(self, x):
        return self.y[self.step(x)]

    @classmethod
    def from_sequence(cls, y, step, y_dtype=None):
        return cls(array(y, dtype=y_dtype), step)


    @classmethod
    def from_step(cls, step, y_dtype=None):
        y = OrderedDict()
        step_y = []
        for i in step.iter_terms():
            step_y.append(y.setdefault(i[0], len(y)))
        return cls.from_sequence(
            y = tuple(y),
            step = StepFunction.from_sequences(
                x = step.x,
                y = step_y,
                y_dtype = 'int',
            ),
            y_dtype = y_dtype,
        )


    @classmethod
    def from_terms(cls, terms, y_dtype=None, x_dtype=None):
        return cls.from_step(StepFunction.from_terms(terms, y_dtype, x_dtype))


    @classmethod
    def from_intervals(cls, intervals, y_dtype='bool'):
        return cls.from_sequence((True, False), StepFunction.from_intervals(intervals, 'int'), y_dtype)

    def iter_terms(self):
        for i in self.step.iter_terms():
            yield (self.y[i[0]], i[1])

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
