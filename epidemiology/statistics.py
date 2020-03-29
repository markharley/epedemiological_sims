from typing import List

import pandas as pd

from .agent import Agent


filters = {
    'infected': lambda a: a.infectious,
    'symptomatic': lambda a: a.symptomatic,
    'dead': lambda a: not a.alive,
    'recovered': lambda a: a.immune and a.alive,
    'alive': lambda a: a.alive,
    'susceptible': lambda a: a.alive and not (a.infectious or a.immune),
    'removed': lambda a: a.immune or not a.alive,
}


class Statistics:
    def __init__(self):
        self.data = pd.DataFrame(columns=list(filters.keys()))

    def collect(self, agents: List[Agent]) -> None:
        stats = {
            col: sum(1 for a in agents if filter_(a))
            for col, filter_ in filters.items()
        }
        print(stats)
        self.data = self.data.append(stats, ignore_index=True)

    def series(self, key: str) -> pd.Series:
        return self.data[[key]]
