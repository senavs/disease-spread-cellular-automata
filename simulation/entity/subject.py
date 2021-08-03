import numpy as np

from simulation.entity.prevention import PreventionGroup, PreventionABC
from simulation.settings import SubjectSettings
from simulation.entity.pathology import PathologyABC, NullPathology
from simulation.entity.state import SubjectState, draw_colors


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
        self.state = SubjectState.NORMAL

        self.disease: PathologyABC = NullPathology(self)
        self.prevention: PreventionGroup = PreventionGroup()

    def contact(self, subjects: list['Subject']):
        """Create contact with others subject and the disease try to infect all"""

        for subject in subjects:
            if subject == self:  # cannot contact with it self
                continue
            self.disease.infect(subject)

    def include_prevention(self, *preventions: PreventionABC):
        """Include new prevention to group"""
        self.prevention.include(*preventions)

    def remove_prevention(self, *preventions: PreventionABC):
        """Remove a prevention from group"""
        self.prevention.remove(*preventions)

    def draw(self):
        """Return subject color based on status"""

        return draw_colors[self.state]

    def __bool__(self):
        """True if subject is sick"""
        return self.state in (SubjectState.EXPOSED, SubjectState.INFECTIOUS)

    def __str__(self):
        return f'Subject({self.id}, {self.age}, {self.state}, {self.disease})'

    def __repr__(self):
        return self.__str__()
