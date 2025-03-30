import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.holtwinters import (
    ExponentialSmoothing,
    HoltWintersResults,
)

from .estimator import Estimator, ParameterInfo


def holt_winters_multiplicative(
    data: pd.DataFrame,
    value_column_name: str,
    date_column_name: str,
    seasonal_periods: int,
) -> Estimator:
    model = ExponentialSmoothing(
        data[value_column_name],
        dates=data[date_column_name],
        freq="D",
        trend="multiplicative",
        seasonal="multiplicative",
        seasonal_periods=seasonal_periods,
    ).fit(method="ls")

    return Estimator(
        base_model=model,
        residuals=model.resid,
        predict=model.predict,
        rmse=_compute_rmse(model, data),
        r_squared=_compute_r_squared(model, data[value_column_name]),
        parameters=_compute_params_ci(model),
    )


def _compute_rmse(
    model: HoltWintersResults,
    data: pd.DataFrame,
) -> float:
    degrees_of_freedom = len(data) - 1
    return np.sqrt(model.sse / degrees_of_freedom)


def _compute_r_squared(
    model: HoltWintersResults,
    values: pd.Series,
) -> float:
    sst = np.sum((values - np.mean(values)) ** 2)
    return 1 - (model.sse / sst)


def _compute_params_ci(model: HoltWintersResults) -> list[ParameterInfo]:
    jacobian = model.mle_retvals.get("jac")
    assert jacobian is not None, "Gradient not available in model results."

    jacobian = np.array(jacobian)
    JtJ_inv = np.linalg.inv(jacobian.T @ jacobian)

    residuals = model.resid
    sigma2 = np.var(residuals, ddof=1)

    cov_matrix = JtJ_inv * sigma2

    standard_errors = np.sqrt(np.diag(cov_matrix))
    level_se, trend_se, seasonal_se, *_ = standard_errors

    model_params = model.params

    degrees_of_freedom = len(model.resid) - 1

    params = ("smoothing_level", "smoothing_trend", "smoothing_seasonal")

    parameter_infos = []
    for param, standard_error in zip(params, standard_errors, strict=False):
        if param not in model_params:
            raise ValueError(f"Parameter {param} not found in model parameters.")
        param_value = model_params[param]
        parameter_info = _compute_ci_for_parameter(
            param_value=param_value,
            standard_error=standard_error,
            name=param,
            degrees_of_freedom=degrees_of_freedom,
        )
        parameter_infos.append(parameter_info)

    return parameter_infos


def _compute_ci_for_parameter(
    param_value: float,
    standard_error: float,
    name: str,
    degrees_of_freedom: int,
    confidence=0.95,
):
    critical_t_statistic = stats.t.ppf(1 - (1 - confidence) / 2, df=degrees_of_freedom)

    level_margin_of_error = critical_t_statistic * standard_error

    lower_bound_ci = param_value - level_margin_of_error
    upper_bound_ci = param_value + level_margin_of_error

    t_statistic = param_value / standard_error
    p_value = (1 - stats.t.cdf(abs(t_statistic), df=degrees_of_freedom)) * 2

    return ParameterInfo(
        name=name,
        value=param_value,
        standard_error=standard_error,
        ci=(lower_bound_ci, upper_bound_ci),
        t_statistic=t_statistic,
        p_value=p_value,
    )
