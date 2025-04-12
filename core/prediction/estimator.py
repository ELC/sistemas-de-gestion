from collections.abc import Callable, Collection, Sequence
from typing import Any

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, computed_field


class ParameterInfo(BaseModel):
    name: str
    value: float
    standard_error: float
    ci: tuple[float, float]
    t_statistic: float
    p_value: float
    confidence_level: float = 0.95

    def __bool__(self) -> bool:
        return not bool(np.isnan(self.t_statistic))

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.value:.4f} - "
            f"{self.confidence_level:.0%} CI: [{self.ci[0]:.4f}, {self.ci[1]:.4f}] - "
            f"t-statistic: {self.t_statistic:.4f} - "
            f"p-value: {self.p_value:.4f}"
        )


class Estimator(BaseModel):
    """
    This is a facade model to unify different interfaces among models from
    different libraries
    """

    base_model: Any
    residuals: Collection[float]
    predict: Callable[[int, int], pd.Series]
    r_squared: float
    parameters: Sequence[ParameterInfo]
    degrees_of_freedom: int
    summary: str

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @property
    @computed_field
    def rmse(self) -> float:
        return np.sqrt(np.mean(np.array(self.residuals) ** 2))
