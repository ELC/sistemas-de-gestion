from typing import Iterable

import scipy.stats as stats
from statsmodels.stats import diagnostic


def normality_test(data: Iterable[float], significance_level: float = 0.05) -> None:
    assert 0 < significance_level < 1, "Significance level must be between 0 and 1."

    sample_size = len(data)

    if sample_size > 50:
        kolmogorov_statistic, p_value = diagnostic.lilliefors(data)
        print(
            f"Kolmogorov-Smirnov statistic with Lilliefors correction: {kolmogorov_statistic:.4f}"
        )
    else:
        shapiro_statistic, p_value = stats.shapiro(data)
        print(f"Shapiro-Wilk statistic: {shapiro_statistic:.4f}")

    print(f"p-value: {p_value:.4f}")
    reject_null_hypothesis = p_value < significance_level

    if reject_null_hypothesis:
        print("Reject null hypothesis: The data are not normally distributed.")
        return
    
    print("Fail to reject null hypothesis: The data may be normally distributed.")
