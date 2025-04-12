from collections.abc import Iterable

from statsmodels.graphics import tsaplots
from statsmodels.tsa import stattools


def compute_autocorrelation(data: Iterable[float]) -> None:
    acf_values = stattools.acf(data, nlags=5, fft=False, qstat=True, alpha=0.05)
    for index, values in enumerate(zip(*acf_values, strict=False)):
        if index == 0:
            continue

        autocorrelation, confidence_internal, _, p_value = values
        lower_bound_ci, upper_bound_ci = confidence_internal
        print(
            f"Lag {index}: {autocorrelation:>7.3f} - "
            f"95% CI: [{lower_bound_ci:6.3f}, {upper_bound_ci:6.3f}] - "
            f"p-value: {p_value:.3f}"
        )

    tsaplots.plot_acf(data, lags=list(range(1, 6)))
