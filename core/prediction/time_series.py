from collections.abc import Collection, Iterable

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.exponential_smoothing.ets import ETSModel, ETSResults
from statsmodels.tsa.holtwinters import ExponentialSmoothing, Holt, HoltWintersResults

from .estimator import Estimator, ParameterInfo


def forecast_multiplicative_trend_and_seasonal(
    data: pd.DataFrame,
    value_column_name: str,
    date_column_name: str,
    seasonal_periods: int,
) -> Estimator:
    model = ETSModel(
        data[value_column_name],
        dates=data[date_column_name],
        freq="D",
        trend="multiplicative",
        seasonal="multiplicative",
        seasonal_periods=seasonal_periods,
    ).fit()

    return Estimator(
        base_model=model,
        residuals=model.resid,
        predict=model.predict,
        r_squared=_compute_r_squared(model, data[value_column_name]),
        parameters=_compute_params_ci(
            model, params=("smoothing_level", "smoothing_trend", "smoothing_seasonal")
        ),
        degrees_of_freedom=model.df_resid,
        summary=model.summary().as_text(),
    )


def forecast_additive_seasonal(
    data: pd.DataFrame,
    value_column_name: str,
    date_column_name: str,
    seasonal_periods: int,
) -> Estimator:
    model = ExponentialSmoothing(
        data[value_column_name].to_numpy(),
        dates=data[date_column_name].to_numpy(),
        freq="D",
        trend=None,
        seasonal="additive",
        seasonal_periods=seasonal_periods,
    ).fit(method="ls")

    number_of_parameters = model.mle_retvals.jac.shape[1]
    degrees_of_freedom = len(data) - number_of_parameters

    return Estimator(
        base_model=model,
        residuals=model.resid,
        predict=model.predict,
        r_squared=_compute_r_squared(model, data[value_column_name]),
        parameters=_compute_params_ci_from_jacobian(model, len(data)),
        degrees_of_freedom=degrees_of_freedom,
        summary=model.summary().as_text(),
    )


def forecast_simple(
    data: pd.DataFrame,
    value_column_name: str,
) -> Estimator:
    model = Holt(data[value_column_name]).fit(method="ls")

    number_of_parameters = model.mle_retvals.jac.shape[1]
    degrees_of_freedom = len(data) - number_of_parameters

    return Estimator(
        base_model=model,
        residuals=model.resid,
        predict=model.predict,
        r_squared=_compute_r_squared(model, data[value_column_name]),
        parameters=_compute_params_ci_from_jacobian(model, len(data)),
        degrees_of_freedom=degrees_of_freedom,
        summary=model.summary().as_text(),
    )


def _compute_r_squared(
    model: ETSResults,
    values: Iterable[float],
) -> float:
    sst = np.sum((values - np.mean(values)) ** 2)
    return 1 - (model.sse / sst)


def _compute_params_ci_from_jacobian(
    model: HoltWintersResults,
    data_lenght: int,
) -> list[ParameterInfo]:
    degrees_of_freedom = _compute_degrees_of_freedom(model, data_lenght)
    standard_errors = _compute_standard_errors(model)
    parameters = model.params_formatted.itertuples()
    param_infos = []
    for row, standard_error in zip(parameters, standard_errors, strict=False):
        param_info = _compute_ci_for_parameter_from_jacobian(
            row.param,
            row.name,
            degrees_of_freedom,
            standard_error,
        )
        if not param_info:
            continue
        param_infos.append(param_info)
    return param_infos


def _compute_degrees_of_freedom(model: HoltWintersResults, data_lenght: int) -> int:
    jacobian = model.mle_retvals.jac
    number_of_parameters = jacobian.shape[1]
    return data_lenght - number_of_parameters


def _compute_standard_errors(model: HoltWintersResults) -> Collection[float]:
    residuals = model.resid
    jacobian = model.mle_retvals.jac
    number_of_parameters = jacobian.shape[1]
    sigma_squared = np.var(np.array(residuals), ddof=number_of_parameters)
    JTJ_inv = np.linalg.inv(jacobian.T @ jacobian)
    covariance_matrix = sigma_squared * JTJ_inv
    return np.sqrt(np.diag(covariance_matrix))


def _compute_ci_for_parameter_from_jacobian(
    param_value: float,
    param_name: str,
    degrees_of_freedom: int,
    standard_error: float,
    significance: float = 0.05,
) -> ParameterInfo:
    critical_t = stats.t.ppf(1 - significance / 2, df=degrees_of_freedom)
    lower_bound_ci = param_value - critical_t * standard_error
    upper_bound_ci = param_value + critical_t * standard_error
    t_statistic = param_value / standard_error
    single_tailed_p_value = 1 - stats.t.cdf(np.abs(t_statistic), df=degrees_of_freedom)
    two_tailed_p_value = 2 * single_tailed_p_value

    return ParameterInfo(
        name=param_name,
        value=param_value,
        standard_error=standard_error,
        ci=(lower_bound_ci, upper_bound_ci),
        t_statistic=t_statistic,
        p_value=two_tailed_p_value,
    )


def _compute_params_ci(
    model: ETSResults, params: Collection[str]
) -> list[ParameterInfo]:
    assert all(param in model.param_names for param in params), (
        f"{params} not subset of {model.param_names}"
    )

    return [_compute_ci_for_parameter(model, param) for param in params]


def _compute_ci_for_parameter(
    model: ETSResults,
    param: str,
    significance: float = 0.05,
) -> ParameterInfo:
    param_index = model.param_names.index(param)
    degrees_of_freedom = model.df_resid

    critical_t_statistic = stats.t.ppf(1 - significance / 2, df=degrees_of_freedom)
    standard_error = model.bse[param_index]
    level_margin_of_error = critical_t_statistic * standard_error

    param_value = model.params[param_index]
    lower_bound_ci = param_value - level_margin_of_error
    upper_bound_ci = param_value + level_margin_of_error

    t_statistic = model.tvalues[param_index]

    one_tailed_p_value = 1 - stats.t.cdf(abs(t_statistic), df=degrees_of_freedom)
    two_tailed_p_value = one_tailed_p_value * 2

    return ParameterInfo(
        name=param,
        value=param_value,
        standard_error=standard_error,
        ci=(lower_bound_ci, upper_bound_ci),
        t_statistic=t_statistic,
        p_value=two_tailed_p_value,
    )


def brown_model(series: pd.Series, alpha: float) -> pd.Series:
    s1 = series.ewm(alpha=alpha).mean()
    s2 = s1.ewm(alpha=alpha).mean()

    at = 2 * s1 - s2
    bt = (alpha / (1 - alpha)) * (s1 - s2)

    forecast = (at + bt).shift(1)
    forecast.iloc[0] = series.iloc[0]
    return forecast
