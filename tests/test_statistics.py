import numpy as np
import pytest

from epidemiology.agent import Agent
from epidemiology.statistics import Statistics


@pytest.fixture
def new_stats():
    return Statistics()


@pytest.fixture
def agents():
    return [Agent((0, 0), 1.0) for _ in range(10)]


@pytest.fixture
def stats(agents, new_stats):
    stats = new_stats
    stats.collect(agents)

    agents[0].contract(p_symptoms=1.0)
    agents[1].contract(p_symptoms=0.0)
    agents[2].alive = False
    agents[3].immune = True
    stats.collect(agents)
    return stats


def check_count(
    stats: Statistics,
    key: str,
    expected: int,
    start: int = 0,
) -> None:
    values = stats.series(key).values
    assert np.array_equal(values, np.array([[start], [expected]]))


def test_collects_infected(stats):
    check_count(stats, 'infected', 2)


def test_collects_symptomatic(stats):
    check_count(stats, 'symptomatic', 1)


def test_collects_dead(stats):
    check_count(stats, 'dead', 1)


def test_collects_recovered(stats):
    check_count(stats, 'recovered', 1)


def test_collects_alive(agents, stats):
    num_agents = len(agents)
    check_count(stats, 'alive', num_agents - 1, start=num_agents)


def test_collects_susceptible(agents, stats):
    num_agents = len(agents)
    check_count(stats, 'susceptible', num_agents - 4, start=num_agents)


def test_collects_removed(stats):
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    check_count(stats, 'removed', 2)
