from typing import Any, Callable, Sequence

import pandas as pd
from pydantic import BaseModel, ConfigDict


class ParameterInfo(BaseModel):
    name: str
    value: float
    standard_error: float
    ci: tuple[float, float]
    t_statistic: float
    p_value: float

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.value:.4f} ± {self.standard_error:.4f} "
            f"({self.ci[0]:.4f}, {self.ci[1]:.4f}) - "
            f"t-statistic: {self.t_statistic:.4f} - "
            f"p-value: {self.p_value:.4f}"
        )


class Estimator(BaseModel):
    """
    This is a facade model to unify different interfaces among models from
    different libraries
    """

    base_model: Any
    residuals: pd.Series
    predict: Callable[[int, int], pd.Series]
    rmse: float
    r_squared: float
    parameters: Sequence[ParameterInfo]
    degrees_of_freedom: int
    summary: str
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
