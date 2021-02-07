from matplotlib.pyplot import step


def plot_terms(x, color="b"):
    b, a = zip(*x)
    return step(a, b, color, where="post")

def plot_step(x, color="b"):
    return plot_terms(x.iter_terms(), color)
