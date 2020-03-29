from dataclasses import dataclass

import numpy as np


@dataclass
class Box:
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    bounce: float = 2.0

    def contain(
        self,
        pos: np.ndarray,
        shift: np.ndarray
    ) -> np.ndarray:
        new_pos = pos + shift
        if new_pos[0] < self.x_min:
            shift[0] /= -self.bounce
        if new_pos[0] > self.x_max:
            shift[0] /= -self.bounce
        if new_pos[1] < self.y_min:
            shift[1] /= -self.bounce
        if new_pos[1] > self.y_max:
            shift[1] /= -self.bounce
        return pos + shift
