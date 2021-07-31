from enum import Enum

import numpy as np


class SubjectState(str, Enum):
    OK: str = 'OK'
    SICK: str = 'SICK'
    DEAD: str = 'DEAD'


class PathologyState(str, Enum):
    SUSCETIBLE: str = 'SUSCETIBLE'
    EXPOSED: str = 'EXPOSED'
    INFECTIOUS: str = 'INFECTIOUS'
    REMOVED: str = 'REMOVED'


class DrawColors:
    NORMAL: list[int] = np.array([255, 255, 255])
    EXPOSED: list[int] = np.array([255, 255, 0])
    INFECTIOUS: list[int] = np.array([200, 0, 0])
    HEALED: list[int] = np.array([0, 255, 0])
    DEAD: list[int] = np.array([0, 0, 0])
