from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from simulation.settings import PathologySettings, SubjectSettings
from simulation.entity.state import PathologyState, SubjectState

if TYPE_CHECKING:
    from simulation.entity.subject import Subject


class PathologyABC(ABC):
    _days_settled: int = 0

    def __init__(self, subject: Subject):
        self.subject = subject
        self.state = PathologyState.EXPOSED
        self.infection_prob_percentage = float(PathologySettings.INFECTION_PROB_PERCENTAGE)
        self.death_prob_percentage = float(PathologySettings.DEATH_PROB_PERCENTAGE)
        self.max_exposed_days = int(PathologySettings.MAX_EXPOSED_DAYS)
        self.max_infectious_days = int(PathologySettings.MAX_INFECTIOUS_DAYS)

    @abstractmethod
    def infect(self, subject: Subject) -> bool:
        """Try to infect a subject

        Parameters
        ----------
        subject : object
            subject that will be infect (or not)

        Returns
        -------
        bool
            If the subject was infected
        """

    @abstractmethod
    def kill(self) -> bool:
        """Kill the subject with the disease

        It should do:
            - Set PathologyState to REMOVED
            - Set SubjectState to DEAD

        Returns
        -------
        bool
            If the subject was killed
        """

    @abstractmethod
    def progress(self):
        """Consider one day was passed. Evolve pathology.

        It should do:
            - Set subject to OK if the disease passed the limit days and the subject still alive
        """

    def __str__(self):
        return f'Pathology({self.state})'


class NullPathology(PathologyABC):

    def __init__(self, subject: Subject):
        super().__init__(subject)
        self.state = PathologyState.SUSCETIBLE

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
            subject.state = SubjectState.SICK
            return True
        return False

    def should_be_infected(self, subject: Subject) -> bool:
        """Calculate probability of a subject be infected.
        It should consider pathology probs and vaccine probs

        Parameters
        ----------
        subject : object

        Returns
        -------
        prob : bool
            Probability of be infected
        """

        if self.state != PathologyState.INFECTIOUS or \
                subject.state in (SubjectState.SICK, SubjectState.DEAD) or \
                subject.disease.state != PathologyState.SUSCETIBLE:
            return False

        # TODO: consider vaccine
        if random.random() <= self.infection_prob_percentage:
            return True

        return False

    def kill(self) -> bool:
        if self.should_be_dead():
            self.subject.state = SubjectState.DEAD
            self.state = PathologyState.REMOVED
            return True
        return False

    def should_be_dead(self) -> bool:
        """Calculate probability of a subject be dead.
        It should consider pathology probs, age and vaccine probs

        Returns
        -------
        prob : bool
            Probability of be dead
        """

        # TODO: consider vaccine
        if self.subject.state in (SubjectState.OK, SubjectState.DEAD) or self.subject.disease.state == PathologyState.SUSCETIBLE:
            return False

        prob = (self.subject.age * self.death_prob_percentage) / SubjectSettings.LIFE_EXPECTANCY  # considering that people only live 100 years

        if random.random() <= prob:
            return True

        return False

    def progress(self):
        """Consider one day was passed. Evolve pathology"""

        if self.subject.state == SubjectState.SICK:
            self._days_settled += 1
            self.kill()
