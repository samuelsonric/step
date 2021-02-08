from step.terms import reduce_terms
from step.step import StepFunction
from numpy import ones, arange, unique, array, eye, nan_to_num
from functools import cached_property
from math import inf

class PullBack:
    def __init__(self, mtx, x):
        self.mtx = mtx
        self.x = x

    @classmethod
    def from_step(cls, step):
        return cls(*pull_back_0(step)[:-1]) 

    def __matmul__(self, other):
        if other.ndim > 1:
            return PullBack(self.mtx @ other, self.x)
        else:
            return StepFunction.from_terms(zip(self.mtx @ other, self.x))
        
    @cached_property
    def preimg(self):
        return tuple(map(self.__matmul__, eye(self.mtx.shape[1])))

    # TODO
    def __mul__(self, other):
        raise NotImplementedError

'''
def pull_back_0(step):
    a, col_ind = unique(step.y, return_inverse=True)
    data = ones(len(col_ind), dtype='bool')
    row_ind = arange(len(col_ind), dtype='int')

    return (csc_matrix((data, (row_ind, col_ind))), step.x, a)
'''


def pull_back(step):
    mtx, x, a = pull_back_0(step)
    return (PullBack(mtx, x), a)


def pull_back_0(step):
    a, col_ind = unique(step.y, return_inverse=True)
    id_ = eye(len(a))
    mtx = array(tuple(map(id_.__getitem__, col_ind)))
    return (mtx, step.x, a)


def conditional_kernel(m, x, y):
    return conditional_kernel_0(m, x.preimg, y.preimg)

def conditional_kernel_0(m, x_preimg, y_preimg):
    a = array(tuple(tuple(m @ (i * j) for j in y_preimg) for i in x_preimg))
    s = a.sum(axis=1).reshape(-1, 1)
    s[s==0] = 1
    return a/s


