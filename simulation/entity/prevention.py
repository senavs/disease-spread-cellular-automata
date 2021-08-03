from abc import ABC
from functools import reduce
from operator import mul

from simulation.settings import PreventionSettings


class PreventionABC(ABC):

    def __init__(self, infection_prob_percentage: float, death_prob_percentage: float):
        self.infection_prob_percentage = float(infection_prob_percentage)
        self.death_prob_percentage = float(death_prob_percentage)

    def get_infection_prob(self) -> float:
        """Return prob of be infected"""
        return self.infection_prob_percentage

    def get_death_prob(self) -> float:
        """Return prob of be dead"""
        return self.death_prob_percentage


class PreventionGroup(PreventionABC):

    def __init__(self, *preventions: PreventionABC):
        self.preventions = set(preventions)
        super().__init__(1, 1)

    def get_infection_prob(self) -> float:
        if not self.preventions:
            return 1.
        return reduce(mul, (prevention.get_infection_prob() for prevention in self.preventions))

    def get_death_prob(self) -> float:
        if not self.preventions:
            return 1.
        return reduce(mul, (prevention.get_death_prob() for prevention in self.preventions))

    def include(self, *preventions: PreventionABC):
        for prevention in preventions:
            self.preventions.add(prevention)

    def remove(self, *preventions: PreventionABC):
        for prevention in preventions:
            self.preventions.remove(prevention)


class Vaccine(PreventionABC):

    def __init__(self):
        super().__init__(
            PreventionSettings.VACCINE_INFECTION_PRO_PERCENTAGE,
            PreventionSettings.VACCINE_DEATH_PRO_PERCENTAGE
        )


class SocialIsolation(PreventionABC):

    def __init__(self):
        super().__init__(
            PreventionSettings.SOCIAL_ISOLATION_INFECTION_PRO_PERCENTAGE,
            PreventionSettings.SOCIAL_ISOLATION_DEATH_PRO_PERCENTAGE
        )
