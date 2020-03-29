from typing import List

import numpy as np

from .agent import Agent, AgentStates
from .box import Box
from .disease import Disease
from .statistics import Statistics


def simulate(
    agents: List[Agent],
    agent_states: AgentStates,
    box: Box,
    disease: Disease,
    statistics: Statistics,
):
    timestep = 0
    while True:
        agent_states.collect(agents, timestep)

        infectious = [a for a in agents if a.infectious and a.alive]
        if not infectious:
            break

        neighbours = {
            agent: get_agents_in_range(
                agent,
                agents,
                disease.infect_range,
            )
            for agent in agents
        }

        # Move 'em
        for agent in agents:
            agent.move(box, neighbours[agent])

        # Infect 'em
        for agent in infectious:
            this_neighbours = neighbours[agent]
            for neighbour in this_neighbours:
                if np.random.random() <= disease.p_infect:
                    neighbour.contract(disease.p_symptoms)

        # "Heal" 'em
        for agent in infectious:
            agent.recover(disease.p_death, disease.p_recover)

        statistics.collect(agents)
        timestep += 1


def get_agents_in_range(
    agent: Agent,
    agents: List[Agent],
    infect_range: float,
) -> List[Agent]:
    in_range = []
    for other in agents:
        if not other.alive:
            continue
        between = other.pos - agent.pos
        distance = np.sqrt(np.dot(between, between))
        if distance <= infect_range:
            in_range.append(other)
    return in_range
