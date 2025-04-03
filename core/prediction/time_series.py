from collections.abc import Collection

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.exponential_smoothing.ets import ETSModel, ETSResults

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
        rmse=np.sqrt(model.mse),
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
    model = ETSModel(
        data[value_column_name],
        dates=data[date_column_name],
        freq="D",
        trend=None,
        seasonal="additive",
        seasonal_periods=seasonal_periods,
    ).fit()

    return Estimator(
        base_model=model,
        residuals=model.resid,
        predict=model.predict,
        rmse=np.sqrt(model.mse),
        r_squared=_compute_r_squared(model, data[value_column_name]),
        parameters=_compute_params_ci(
            model, params=("smoothing_level", "smoothing_seasonal")
        ),
        degrees_of_freedom=model.df_resid,
        summary=model.summary().as_text(),
    )


def forecast_simple(
    data: pd.DataFrame,
    value_column_name: str,
    date_column_name: str,
    seasonal_periods: int,
) -> Estimator:
    model = ETSModel(
        data[value_column_name],
        dates=data[date_column_name],
        freq="D",
        error="additive",
        trend=None,
        seasonal=None,
        seasonal_periods=seasonal_periods,
    ).fit()

    return Estimator(
        base_model=model,
        residuals=model.resid,
        predict=model.predict,
        rmse=np.sqrt(model.mse),
        r_squared=_compute_r_squared(model, data[value_column_name]),
        parameters=_compute_params_ci(model, params=("smoothing_level",)),
        degrees_of_freedom=model.df_resid,
        summary=model.summary().as_text(),
    )


def _compute_r_squared(
    model: ETSResults,
    values: pd.Series,
) -> float:
    sst = np.sum((values - np.mean(values)) ** 2)
    return 1 - (model.sse / sst)


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
):
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
