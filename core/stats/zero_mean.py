from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from .descriptive import DescriptiveStatistics


def zero_mean_test(
    data: Iterable[float],
    descriptive_stats: DescriptiveStatistics,
    degrees_of_freedom: int,
    significance_level: float = 0.05,
) -> None:
    t_statistic, p_value = stats.ttest_1samp(data, 0)

    lower_bound_ci, upper_bound_ci = stats.t.interval(
        0.95,
        degrees_of_freedom,
        loc=descriptive_stats.mean,
        scale=descriptive_stats.standard_error,
    )

    print(f"Data mean: {descriptive_stats.mean:.4f}")
    print(f"t-statistics: {t_statistic:.4f}")
    print(f"p-value: {p_value:.4f}")
    print(f"95% CI for Residual Mean: [{lower_bound_ci:.4f}, {upper_bound_ci:.4f}]")

    reject_null_hypothesis = p_value < significance_level

    if reject_null_hypothesis:
        print("Reject null hypothesis: The data do not have zero mean.")
    else:
        print("Fail to reject null hypothesis: The data may have zero mean.")

    df = pd.DataFrame({"data": data})
    sns.pointplot(
        data=df.assign(group=1),
        x="group",
        y="data",
        errorbar=lambda _: (lower_bound_ci, upper_bound_ci),
        estimator=np.mean,
        capsize=0.4,
        n_boot=1e4,
    )
    plt.xlabel("")
    plt.show()
