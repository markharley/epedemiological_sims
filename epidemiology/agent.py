import uuid
from enum import Enum
from typing import List

import numpy as np
import pandas as pd

from .box import Box


class States(Enum):
    healthy = 0
    asymptomatic = 1
    symptomatic = 2
    immune = 3
    dead = 4


class Agent:
    def __init__(
        self,
        pos: np.ndarray,
        speed: float,
        infectious: bool = False,
    ):
        self.uid = uuid.uuid4()
        self.pos = np.asarray(pos)
        self.speed = speed
        self.infectious = infectious

        self.alive = True
        self.immune = False
        self._symptomatic = False
        self.movement = move_normal

        self.days_infected = 0

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.uid == other.uid

    @property
    def symptomatic(self):
        return self.infectious and self._symptomatic

    def contract(self, p_symptoms: float):
        if self.immune or not self.alive:
            return
        self.infectious = True
        self._symptomatic = False
        if np.random.random() <= p_symptoms:
            self._symptomatic = True

    def move(self, box: Box, neighbours: List["Agent"]):
        if not self.alive:
            return
        shift = self.movement(self.speed)
        self.pos = box.contain(self.pos, shift)

    def recover(self, p_death: float, p_recover: float):
        if not self.infectious:
            return
        elif self.symptomatic and np.random.random() <= p_death:
            self.alive = False
        elif np.random.random() <= p_recover:
            self.infectious = False
            self.immune = True
        self.days_infected += 1

    @property
    def state(self):
        if not self.alive:
            return States.dead
        elif self.immune:
            return States.immune
        elif self.infectious and not self.symptomatic:
            return States.asymptomatic
        elif self.symptomatic:
            return States.symptomatic
        return States.healthy

    def to_state_dict(self, timestep: int):
        return {
            'uid': str(self.uid),
            'timestep': timestep,
            'x': self.pos[0],
            'y': self.pos[1],
            'infectious': self.infectious,
            'symptomatic': self.symptomatic,
            'immune': self.symptomatic,
            'dead': not self.alive,
            'state': self.state.name,
            'days_infected': self.days_infected,
        }


def move_normal(speed: float) -> np.ndarray:
    direction = np.random.rand(2) - np.array((0.5, 0.5))
    magnitude = np.sqrt(np.dot(direction, direction))
    return speed * direction / magnitude


class AgentStates:
    def __init__(self):
        self.states = pd.DataFrame()

    def collect(self, agents: List[Agent], timestep: int) -> None:
        states = [a.to_state_dict(timestep) for a in agents]
        self.states = self.states.append(states, ignore_index=True)
