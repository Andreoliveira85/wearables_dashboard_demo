"""
config.py
---------
All the "look and feel" of the dashboard lives here.
Change the values below to customise YOUR dashboard - no other file needs to change.
"""

from dataclasses import dataclass, field


@dataclass
class Theme:
    """A small container for every style choice of the app."""
    title: str = "Wearable Health Monitor"
    subtitle: str = "Sleep, activity and heart rate from 250 users across Europe"
    bootstrap_theme: str = "CYBORG"        # dark themes: DARKLY, SLATE, VAPOR, SUPERHERO, CYBORG
    plotly_template: str = "plotly_dark"   # must match: dark bootstrap theme -> "plotly_dark"
    # NOTE: assets/style.css has a dark background, so light themes (FLATLY, MINTY, LUX)
    # also need style.css changed, otherwise the text is unreadable.
    accent_color: str = "#00E5A8"          # main highlight colour (KPI values, lines)
    font_family: str = "Inter, sans-serif"
    palette: list = field(default_factory=lambda: [
        "#00E5A8", "#5B8DEF", "#FFB547", "#FF6B8B", "#B48CFF", "#4DD0E1", "#F4E04D", "#9AA5B1",
    ])


# The one theme object the whole app imports
THEME = Theme()

# Where the data lives
DATA_PATH = "data/wearables_daily.csv"

# Metrics the user can choose in the dashboard: column name -> nice label
METRICS = {
    "steps": "Steps",
    "sleep_hours": "Sleep (hours)",
    "resting_hr": "Resting heart rate (bpm)",
    "hrv_ms": "HRV (ms)",
    "stress_score": "Stress score",
}