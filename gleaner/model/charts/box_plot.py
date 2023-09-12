import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined
from .base_chart import BaseChart


class BoxPlot(BaseChart):
    def display(self) -> Chart:
        dict_x = {
            "field": self.altair_token.x.name,
            "type": self.altair_token.x.type,
            "axis": alt.Axis(
                format="~s"
                if self.altair_token.y.type == "quantitative"
                else Undefined
            ),
        }

        dict_y = {
            "field": self.altair_token.y.name,
            "type": self.altair_token.y.type,
            "axis": alt.Axis(
                format="~s"
                if self.altair_token.y.type == "quantitative"
                else Undefined
            ),
        }

        if self.altair_token.x.type == "nominal":
            x = alt.Y(**dict_x)
            y = alt.X(**dict_y)

        else:
            x = alt.X(**dict_x)
            y = alt.Y(**dict_y)

        return alt.Chart(self.df, title=self.title).mark_boxplot().encode(x, y)
