import os
from uuid import uuid4


class SystemSettings:
    IMAGE_OUTPUT_PATH: str = f'outputs/{uuid4()}'

    os.makedirs(IMAGE_OUTPUT_PATH, exist_ok=True)


class PathologySettings:
    INFECTION_PROB_PERCENTAGE: float = 0.15
    DEATH_PROB_PERCENTAGE: float = 1
    MAX_EXPOSED_DAYS: float = 6
    MAX_INFECTIOUS_DAYS: float = 14


class BoardSettings:
    DIMENSION: int = 9
    SICK_SUBJECT_LOCATION: int = None  # None is the center. It's like board[4, 4] position (with board 9 dimension)


class SubjectSettings:
    MIN_AGE: int = 10
    MAX_AGE: int = 90
    LIFE_EXPECTANCY: int = 76
