from enum import Enum


class SubjectState(Enum):
    NORMAL = 'NORMAL'
    EXPOSED = 'EXPOSED'
    INFECTIOUS = 'INFECTIOUS'
    HEALED = 'HEALED'
    DEAD = 'DEAD'


draw_colors = {
    'NORMAL': [255, 255, 255],
    'EXPOSED': [200, 100, 0],
    'INFECTIOUS': [150, 0, 0],
    'HEALED': [0, 255, 0],
    'DEAD': [0, 0, 0],
}
