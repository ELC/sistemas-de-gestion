from typing import Iterable

import seaborn as sns
from statsmodels.sandbox.stats import runs


def randomness_test(data: Iterable[float], significance: float = 0.05) -> None:
    z_stats, p_value = runs.runstest_1samp(data)
    print(f"z-statistic: {z_stats:.3f}")
    print(f"p-value: {p_value:.3f}")

    reject_null_hypothesis = p_value < significance

    if reject_null_hypothesis:
        print("Reject null hypothesis: The data are not randomly distributed.")
    else:
        print("Fail to reject null hypothesis: The data may be randomly distributed.")

    sns.scatterplot(data)
