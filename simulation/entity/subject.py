import numpy as np

from simulation.settings import SubjectSettings
from simulation.entity.pathology import PathologyABC, NullPathology
from simulation.entity.state import SubjectState, PathologyState, DrawColors


class Subject:

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '__counter', None):
            setattr(cls, '__counter', 1)
        instance = super().__new__(cls)
        instance.id = getattr(cls, '__counter')
        setattr(cls, '__counter', instance.id + 1)
        return instance

    def __init__(self):
        self.age = int(np.random.uniform(SubjectSettings.MIN_AGE, SubjectSettings.MAX_AGE, 1))
        self.state = SubjectState.OK
        self.disease: PathologyABC = NullPathology(self)

    def contact(self, subjects: list['Subject']):
        for subject in subjects:
            if subject == self:  # cannot contact with it self
                continue
            self.disease.infect(subject)

    def draw(self):
        if self.disease.state == PathologyState.SUSCETIBLE:
            return DrawColors.NORMAL
        elif self.disease.state == PathologyState.EXPOSED:
            return DrawColors.EXPOSED
        elif self.disease.state == PathologyState.INFECTIOUS:
            return DrawColors.INFECTIOUS
        elif self.disease.state == PathologyState.REMOVED:
            return DrawColors.HEALED
        else:
            return DrawColors.DEAD

    def __str__(self):
        return f'Subject({self.id}, {self.age}, {self.state}, {self.disease})'

    def __repr__(self):
        return self.__str__()
