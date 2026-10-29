"""
charts.py
---------
One function per figure. Each function receives a DataFrame and returns a Plotly figure.
These are the same plots we made in the notebook - just wrapped in functions.
"""

import plotly.express as px

from config import METRICS, THEME


def style_figure(fig):
    """Apply the same look to every figure (template, font, transparent background)."""
    fig.update_layout(
        template=THEME.plotly_template,
        font_family=THEME.font_family,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text="",
        hovermode="closest",
    )
    return fig


def empty_figure(message="No data for this selection"):
    """Shown when the filters remove all rows."""
    fig = px.scatter()
    fig.add_annotation(text=message, showarrow=False, font_size=16)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style_figure(fig)


def metric_over_time(df, metric="steps"):
    """Daily average of a metric with a 7-day rolling mean."""
    daily = df.groupby("date", as_index=False)[metric].mean()
    daily["7-day average"] = daily[metric].rolling(7, min_periods=1).mean()

    fig = px.line(daily, x="date", y="7-day average",
                  title=f"{METRICS[metric]} over time",
                  labels={"7-day average": METRICS[metric], "date": ""})
    fig.update_traces(line_color=THEME.accent_color, line_width=3)
    # the noisy daily values as a light line in the background
    fig.add_scatter(x=daily["date"], y=daily[metric], mode="lines", name="daily",
                    line=dict(color="rgba(150,150,150,0.35)", width=1))
    fig.update_layout(showlegend=False)
    return style_figure(fig)


def metric_by_device(df, metric="steps"):
    """Box plot of the metric for each device."""
    fig = px.box(df, x="device", y=metric, color="device",
                 title=f"{METRICS[metric]} by device",
                 labels={metric: METRICS[metric], "device": ""},
                 color_discrete_sequence=THEME.palette, points=False)
    fig.update_layout(showlegend=False)
    return style_figure(fig)


def steps_vs_sleep(df):
    """One dot per user: average steps vs average sleep, coloured by age group."""
    per_user = df.groupby(["user_id", "age_group"], as_index=False).agg(
        steps=("steps", "mean"), sleep_hours=("sleep_hours", "mean"),
        resting_hr=("resting_hr", "mean"))
    fig = px.scatter(per_user, x="steps", y="sleep_hours", color="age_group",
                     size="resting_hr", size_max=14, hover_name="user_id",
                     title="Do active people sleep more? (one dot = one user)",
                     labels={"steps": "Avg daily steps", "sleep_hours": "Avg sleep (h)",
                             "age_group": "Age"},
                     category_orders={"age_group": ["20-29", "30-39", "40-49", "50-59", "60+"]},
                     color_discrete_sequence=THEME.palette)
    return style_figure(fig)


def city_map(df, metric="steps"):
    """Bubble map: one bubble per city, size = number of users, colour = metric."""
    per_city = df.groupby(["city", "lat", "lon"], as_index=False).agg(
        users=("user_id", "nunique"), value=(metric, "mean"))
    fig = px.scatter_map(per_city, lat="lat", lon="lon", size="users", color="value",
                         hover_name="city", size_max=40, zoom=3,
                         center={"lat": 48.5, "lon": 6},
                         color_continuous_scale="Tealgrn",
                         map_style="carto-darkmatter" if "dark" in THEME.plotly_template else "carto-positron",
                         title=f"{METRICS[metric]} by city",
                         labels={"value": METRICS[metric]})
    return style_figure(fig)


if __name__ == "__main__":
    # Quick test: python charts.py  -> opens a figure in your browser
    from data import load_data
    fig = metric_over_time(load_data(), "sleep_hours")
    # the figure is transparent (made for the dark dashboard), so give it a background here
    if "dark" in THEME.plotly_template:
        fig.update_layout(paper_bgcolor="#111111", plot_bgcolor="#111111")
    fig.show()

# if __name__ == "__main__":
#     # Quick test: python charts.py  -> opens a figure in your browser
#     from data import load_data
#     metric_by_device(load_data(), "hrv_ms").show()