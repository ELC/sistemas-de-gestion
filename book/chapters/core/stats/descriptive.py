import numpy as np
import pandas as pd
from pydantic import BaseModel
from scipy import stats


class DescriptiveStatistics(BaseModel):
    mean: float
    variance: float
    standard_deviation: float
    standard_error: float
    degrees_of_freedom: int


def compute_descriptive_statistics(data: pd.Series) -> DescriptiveStatistics:
    return DescriptiveStatistics(
        mean=np.mean(data),
        variance=np.var(data, ddof=1),
        standard_deviation=np.std(data, ddof=1),
        standard_error=stats.sem(data, ddof=1),
        degrees_of_freedom=len(data) - 1,
    )
