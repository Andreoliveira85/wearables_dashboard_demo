"""
kpis.py
-------
A tiny class that represents one KPI card (a big number with a label).
"""

import dash_bootstrap_components as dbc
from dash import html

from config import THEME


class KpiCard:
    """One KPI card: a title, a value and an optional unit."""

    def __init__(self, title, value, unit="", icon="📊"):
        self.title = title
        self.value = value
        self.unit = unit
        self.icon = icon

    def formatted_value(self):
        """Nice text for the number: 8,412 or 7.2"""
        if self.value is None:
            return "–"
        if self.value >= 1000 or float(self.value).is_integer():
            return f"{self.value:,.0f}"
        return f"{self.value:.1f}"

    def render(self):
        """Turn the object into Dash components (what the browser shows)."""
        return dbc.Card(
            dbc.CardBody([
                html.Div(f"{self.icon}  {self.title}", className="kpi-title"),
                html.Div([
                    html.Span(self.formatted_value(), style={"color": THEME.accent_color}),
                    html.Span(f" {self.unit}", className="kpi-unit"),
                ], className="kpi-value"),
            ]),
            className="kpi-card",
        )


def safe_mean(series):
    """Mean that returns None for an empty selection instead of NaN."""
    return None if series.dropna().empty else series.mean()


def build_kpis(df):
    """Create the list of KPI cards for the current (filtered) data."""
    return [
        KpiCard("Active users", df["user_id"].nunique(), "", "👥"),
        KpiCard("Avg daily steps", safe_mean(df["steps"]), "", "👟"),
        KpiCard("Avg sleep", safe_mean(df["sleep_hours"]), "h", "🌙"),
        KpiCard("Avg resting HR", safe_mean(df["resting_hr"]), "bpm", "❤️"),
    ]


if __name__ == "__main__":
    # Quick test: python kpis.py
    card = KpiCard("Avg daily steps", 8412.3)
    print(card.title, "->", card.formatted_value())