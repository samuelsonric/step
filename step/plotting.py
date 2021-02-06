from matplotlib.pyplot import step


def plot_terms(x, color="b"):
    b, a = zip(*x)
    return step(a, b, color, where="post")
