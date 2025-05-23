from collections.abc import Collection

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.graphics import gofplots
from statsmodels.stats import diagnostic


def normality_test(data: Collection[float], significance_level: float = 0.05) -> None:
    assert 0 < significance_level < 1, "Significance level must be between 0 and 1."

    kolmogorov_statistic, kolmogorov_p_value = diagnostic.lilliefors(data)
    print(
        "Kolmogorov-Smirnov statistic with "
        f"Lilliefors correction: {kolmogorov_statistic:.4f}"
    )
    print(f"Kolmogorov-Smirnov p-value: {kolmogorov_p_value:.4f}")

    shapiro_statistic, shapiro_p_value = stats.shapiro(data)
    print(f"Shapiro-Wilk statistic: {shapiro_statistic:.4f}")
    print(f"Shapiro-Wilk p-value: {shapiro_p_value:.4f}")

    big_sample_size = 50
    p_value = kolmogorov_p_value if len(data) > big_sample_size else shapiro_p_value
    reject_null_hypothesis = p_value < significance_level

    if reject_null_hypothesis:
        print("Reject null hypothesis: The data are not normally distributed.")
    else:
        print("Fail to reject null hypothesis: The data may be normally distributed.")

    sns.histplot(data=data, kde=True)
    plt.show()

    gofplots.qqplot(data, fit=True, line="45")
    plt.xlim(-3.5, 3.5)
    plt.ylim(-3.5, 3.5)
    plt.show()
