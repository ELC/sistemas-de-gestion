from typing import Callable, NamedTuple

import numpy as np
import numpy.typing as npt

class ODEInfo(NamedTuple):
    coefficient: complex
    initial_value: float
    time_step: float
    time_final: float

    @property
    def time(self) -> npt.NDArray[np.float32]:
        return np.arange(0, self.time_final + self.time_step, self.time_step) 

    @property
    def analytical_solution(self) -> npt.NDArray[np.complex128]:
        return self.initial_value * np.exp(self.coefficient * self.time)
    
    @property
    def title(self) -> str:
        return f"$y' = {self.coefficient}y ; y_0 = {self.initial_value} ; h = {self.time_step}$"
    

ODESolver = Callable[[ODEInfo], tuple[npt.ArrayLike, npt.NDArray[np.complex128]]]
