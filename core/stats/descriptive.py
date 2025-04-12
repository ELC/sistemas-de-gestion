from collections.abc import Iterable

import numpy as np
from pydantic import BaseModel, field_serializer
from scipy import stats


class DescriptiveStatistics(BaseModel):
    mean: float
    variance: float
    standard_deviation: float
    standard_error: float

    @field_serializer(
        "mean", "variance", "standard_deviation", "standard_error", when_used="json"
    )
    @staticmethod
    def serialize_courses_in_order(value: float) -> str:
        return f"{value:.4f}"

    def show(self) -> None:
        print(self.model_dump_json(indent=4))


def compute_descriptive_statistics(data: Iterable[float]) -> DescriptiveStatistics:
    return DescriptiveStatistics(
        mean=np.mean(data),
        variance=np.var(data, ddof=1),
        standard_deviation=np.std(data, ddof=1),
        standard_error=float(stats.sem(data, ddof=1)),
    )
