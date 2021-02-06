from matplotlib.pyplot import step


def plot_terms(x, color="b"):
    b, a = zip(*x)
    return step(a, b, color, where="post")


def plot_simple_function(sfun, color="b"):
    return step(sfun.mat[:, 1], sfun.mat[:, 0], color, where="post")
