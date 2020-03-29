import uuid

import numpy as np

from epidemiology.agent import Agent, AgentStates
from epidemiology.box import Box
from epidemiology.disease import Disease
from epidemiology.simulation import simulate
from epidemiology.statistics import Statistics


def run():
    box = Box(
        x_min=0.0,
        x_max=10.0,
        y_min=0.0,
        y_max=10.0,
    )
    agents = [
        Agent(pos=10 * np.random.rand(2), speed=0.1,)
        for _ in range(1000)
    ]
    agents[0].infectious = True
    disease = Disease(
        uuid.uuid4(),
        infect_range=1.0,
        p_infect=0.2,
        p_symptoms=1.0,
        p_death=0.0,
        p_recover=0.1,
    )
    agent_states = AgentStates()
    stats = Statistics()
    simulate(agents, agent_states, box, disease, stats)
    return agent_states, stats


if __name__ == '__main__':
    run()
