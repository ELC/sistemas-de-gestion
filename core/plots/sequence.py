from typing import Any

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import axes

date_formater = mdates.DateFormatter("%U %A")


def plot_sequence(
    data: pd.Series, title: str, ax: axes.Axes | None = None, **kwargs: Any
) -> axes.Axes:
    ax = ax or plt.subplot()
    sns.lineplot(data=data, ax=ax, **kwargs)
    ax.set_title(title)
    ax.set_xlabel("Index")
    ax.set_ylabel(data.name)
    ax.set_ylim(bottom=0)
    ax.grid(True)
    return ax


def plot_sequence_with_date(
    data: pd.DataFrame,
    value_column_name: str,
    date_colum_name: str,
    title: str,
    ax: axes.Axes | None = None,
    **kwargs: Any,
) -> axes.Axes:
    ax = ax or plt.subplot()
    sns.lineplot(data=data, x=date_colum_name, y=value_column_name, ax=ax, **kwargs)
    ax.set_title(title)
    plt.xticks(rotation=-90)
    ax.set_xlabel("Date")
    ax.set_ylabel(data[value_column_name].name)

    xticks = data[date_colum_name].iloc[::5]
    ax.set_xticks(xticks, xticks, rotation=-90)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(date_formater)
    ax.grid(True)
    return ax
