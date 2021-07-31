from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from entity.state import PathologyState, SubjectState

if TYPE_CHECKING:
    from entity.subject import Subject


class PathologyABC(ABC):
    _days_settled: int = 0

    def __init__(
            self,
            subject: Subject,
            infection_prob_percentage: float,
            death_prob_percentage: float,
            max_exposed_days: int,
            max_infectious_days: int
    ):
        self.subject = subject
        self.state = PathologyState.EXPOSED
        self.infection_prob_percentage = float(infection_prob_percentage)
        self.death_prob_percentage = float(death_prob_percentage)
        self.max_exposed_days = int(max_exposed_days)
        self.max_infectious_days = int(max_infectious_days)

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

    # def __str__(self):
    #     return f'Pathology({self.state})'


class NullPathology(PathologyABC):

    def __init__(self, subject: Subject):
        super().__init__(subject, 0, 0, 0, 0)
        self.state = PathologyState.SUSCETIBLE

    def infect(self, subject: Subject) -> bool:
        return False

    def kill(self) -> bool:
        return False

    def progress(self):
        """Consider one day was passed. Evolve pathology"""


class ConcretePathology(PathologyABC):

    def infect(self, subject: Subject) -> bool:
        if self.should_be_infected(subject):
            subject.disease = ConcretePathology(
                subject,
                self.infection_prob_percentage,
                self.death_prob_percentage,
                self.max_exposed_days,
                self.max_infectious_days
            )
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

        prob = (self.subject.age * self.death_prob_percentage) / 100  # considering that people only live 100 years

        if random.random() <= prob:
            return True

        return False

    def progress(self):
        """Consider one day was passed. Evolve pathology"""

        if self.subject.state == SubjectState.SICK:
            self._days_settled += 1
            self.kill()