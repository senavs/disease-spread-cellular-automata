from enum import Enum

import numpy as np


class SubjectState(str, Enum):
    NORMAL: str = 'NORMAL'
    EXPOSED: str = 'EXPOSED'
    INFECTIOUS: str = 'INFECTIOUS'
    HEALED: str = 'HEALED'
    DEAD: str = 'DEAD'


draw_colors = {
    'NORMAL': np.array([255, 255, 255]),
    'EXPOSED': np.array([200, 100, 0]),
    'INFECTIOUS': np.array([150, 0, 0]),
    'HEALED': np.array([0, 255, 0]),
    'DEAD': np.array([0, 0, 0]),
}
