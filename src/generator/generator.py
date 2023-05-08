import numpy as np
import pandas as pd
from numpy.random import choice

from src.generator import PriorParameters
from src.model import Attribute, GleanerChart, GleanerDashboard
from src.config import chart_type, agg_type, chart_map


def p(x: np.ndarray) -> np.ndarray:
    return x / x.sum()


def is_valid_map(current: list, map: list) -> bool:
    return all(
        [
            map[i] == c.type if isinstance(c, Attribute) else map[i] == c
            for i, c in enumerate(current)
        ]
    )


class Generator:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.attrs: list[Attribute | None] = [None] + [
            Attribute(col, "C" if df[col].dtype == "object" else "Q")
            for col in df.columns
        ]
        self.attr_names = [
            e.name if isinstance(e, Attribute) else e for e in self.attrs
        ]
        self.prior = PriorParameters(self.attr_names)

    def initialize(self):
        self.prior = PriorParameters(self.attr_names)

    def attr_mask(self, current: list["Attribute"]):
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array(
            [
                (e is None and e in valid_type)
                or (
                    isinstance(e, Attribute)
                    and e.type in valid_type
                    and e not in current
                )
                for e in self.attrs
            ]
        )
        return weight_mask

    def ct_mask(self, current: list):
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in chart_type])
        return weight_mask

    def at_mask(self, current: list):
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in agg_type])
        return weight_mask

    def sample_one(self) -> GleanerChart:
        current: list = []
        current.append(choice(chart_type, p=p(self.prior.ct.sample())))

        mask_x = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(self.prior.x.sample() * mask_x)))  # type: ignore

        mask_y = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(self.prior.y.sample() * mask_y)))  # type: ignore

        mask_z = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(self.prior.z.sample() * mask_z)))  # type: ignore

        mask_at = self.at_mask(current)
        current.append(choice(agg_type, p=p(self.prior.at.sample() * mask_at)))

        return GleanerChart(current, self.df)

    def sample_dashboard(self, n: int) -> GleanerDashboard:
        return GleanerDashboard([self.sample_one() for _ in range(n)])
