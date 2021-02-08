from matplotlib.pyplot import step


def plot_step(x, color="b"):
    return step(x.x, x.y, color, where="post")
