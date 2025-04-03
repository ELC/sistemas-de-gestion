from typing import Iterable

import numpy as np
from scipy import stats
import seaborn as sns


def constant_variance_test(data: Iterable[float], significance_level: float = 0.05):
    thirds = np.array_split(list(data), 3)
    variances = np.var(thirds, axis=1)
    levene_statistic, p_value = stats.levene(*thirds)

    reject_equal_variance = p_value < significance_level

    print("Variances: " + str([f"{int(v):_d}" for v in variances]))
    print(f"Levene's test statistic: {levene_statistic:.4f}")
    print(f"p-value: {p_value:.4f}")

    if reject_equal_variance:
        print(
            "Reject null hypothesis: Variances are not equal. - Heteroscedasticity detected."
        )
    else:
        print(
            "Fail to reject null hypothesis: Variances may be equal. - Homoscedasticity assumed."
        )

    sns.boxplot(thirds)
    sns.swarmplot(thirds, size=15, color="#333")
