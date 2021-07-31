from enum import Enum


class SubjectState(str, Enum):
    OK: str = 'OK'
    SICK: str = 'SICK'
    DEAD: str = 'DEAD'


class PathologyState(str, Enum):
    SUSCETIBLE: str = 'SUSCETIBLE'
    EXPOSED: str = 'EXPOSED'
    INFECTIOUS: str = 'INFECTIOUS'
    REMOVED: str = 'REMOVED'
