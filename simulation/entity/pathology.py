from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from simulation.settings import PathologySettings, SubjectSettings
from simulation.entity.state import SubjectState

if TYPE_CHECKING:
    from simulation.entity.subject import Subject


class PathologyABC(ABC):

    def __init__(self, subject: Subject):
        self.subject = subject
        self.infection_prob_percentage = float(PathologySettings.INFECTION_PROB_PERCENTAGE)
        self.death_prob_percentage = float(PathologySettings.DEATH_PROB_PERCENTAGE)
        self.max_exposed_days = int(PathologySettings.MAX_EXPOSED_DAYS)
        self.max_infectious_days = int(PathologySettings.MAX_INFECTIOUS_DAYS)

        self.days_settled: int = 0

    @abstractmethod
    def infect(self, subject: Subject) -> bool:
        """Try to infect a subject"""

    @abstractmethod
    def kill(self) -> bool:
        """Kill the subject with the disease"""

    @abstractmethod
    def progress(self):
        """Consider one day was passed. Evolve pathology"""

    def __str__(self):
        return f'Pathology({self.days_settled})'


class NullPathology(PathologyABC):

    def infect(self, subject: Subject) -> bool:
        return False

    def kill(self) -> bool:
        return False

    def progress(self):
        pass


class ConcretePathology(PathologyABC):

    def infect(self, subject: Subject) -> bool:
        if self.should_be_infected(subject):
            subject.disease = ConcretePathology(subject)
            subject.state = SubjectState.EXPOSED
            return True
        return False

    def kill(self) -> bool:
        if self.should_be_dead():
            self.subject.state = SubjectState.DEAD
            return True
        return False

    def progress(self):
        """Consider one day was passed. Evolve pathology"""

        self.days_settled += 1

        # can only kill a subject if it have more then 1 day with the pathology
        if self.days_settled > 1 and self.subject.state in (SubjectState.EXPOSED, SubjectState.INFECTIOUS):
            self.kill()
        else:
            return

        # pathology evolving
        if self.subject.state == SubjectState.EXPOSED and self.days_settled > self.max_exposed_days:
            self.subject.state = SubjectState.INFECTIOUS
        elif self.subject.state == SubjectState.INFECTIOUS and (self.days_settled - self.max_exposed_days) > self.max_infectious_days:
            self.subject.state = SubjectState.HEALED

    def should_be_infected(self, subject: Subject) -> bool:
        """Calculate probability of a subject be infected. It should consider pathology prob and vaccine prob"""

        if self.subject.state in (SubjectState.EXPOSED, SubjectState.INFECTIOUS) and subject.state == SubjectState.NORMAL:
            if random.random() <= self.infection_prob_percentage * self.subject.prevention.get_infection_prob():
                return True
        return False

    def should_be_dead(self) -> bool:
        """Calculate probability of a subject be dead. It should consider pathology probs, age and vaccine probs"""

        if self.subject.state in (SubjectState.EXPOSED, SubjectState.INFECTIOUS):
            prob = (self.subject.age * self.death_prob_percentage) / SubjectSettings.LIFE_EXPECTANCY  # considering that people only live 100 years
            prob = prob * self.subject.prevention.get_death_prob()
            if random.random() <= prob:
                return True
        return False
