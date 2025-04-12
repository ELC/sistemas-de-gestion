import matplotlib.pyplot as plt
from cycler import cycler


def init_config() -> None:
    plt.style.use("bmh")

    colors = [
        "darkmagenta",
        "saddlebrown",
        "darkcyan",
        "olivedrab",
        "darkseagreen",
        "darkkhaki",
        "darkgoldenrod",
        "deepskyblue",
        "firebrick",
        "palevioletred",
    ]

    config = {
        "figure.figsize": (23, 8),
        "axes.titlesize": 18,
        "axes.labelsize": 10,
        "lines.linewidth": 2,
        "lines.markersize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.prop_cycle": cycler(color=colors),
    }

    plt.rcParams.update(config)
