from typing import Iterable

import scipy.stats as stats

from .descriptive import DescriptiveStatistics


def zero_mean_test(
    data: Iterable[float],
    descriptive_stats: DescriptiveStatistics,
    significance_level=0.05,
) -> None:
    _, p_value = stats.ttest_1samp(data, 0)

    lower_bound_ci, upper_bound_ci = stats.t.interval(
        0.95,
        descriptive_stats.degrees_of_freedom,
        loc=descriptive_stats.mean,
        scale=descriptive_stats.standard_error,
    )

    print(f"Data mean: {descriptive_stats.mean:.4f}")
    print(f"p-value: {p_value:.4f}")
    print(f"95% CI for Residual Mean: [{lower_bound_ci:.4f}, {upper_bound_ci:.4f}]")

    reject_null_hypothesis = p_value < significance_level

    if reject_null_hypothesis:
        print("Reject null hypothesis: The residuals do not have zero mean.")
        return

    print("Fail to reject null hypothesis: The residuals may have zero mean.")
