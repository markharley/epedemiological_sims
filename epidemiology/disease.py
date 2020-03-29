from dataclasses import dataclass


@dataclass
class Disease:
    name: str
    infect_range: float
    p_infect: float
    p_symptoms: float
    p_death: float
    p_recover: float
