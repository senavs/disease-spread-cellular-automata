from enum import Enum


class SubjectState(str, Enum):
    NORMAL: str = 'NORMAL'
    EXPOSED: str = 'EXPOSED'
    INFECTIOUS: str = 'INFECTIOUS'
    HEALED: str = 'HEALED'
    DEAD: str = 'DEAD'


draw_colors = {
    'NORMAL': [255, 255, 255],
    'EXPOSED': [200, 100, 0],
    'INFECTIOUS': [150, 0, 0],
    'HEALED': [0, 255, 0],
    'DEAD': [0, 0, 0],
}
