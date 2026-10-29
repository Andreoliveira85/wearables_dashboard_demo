"""
app.py
------
The Dash application: layout (what we see) + callback (what happens when we click).

Run locally:
    python app.py
Then open http://127.0.0.1:8050 in your browser.
"""

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

import charts
from config import METRICS, THEME
from data import filter_data, load_data
from kpis import build_kpis

# ---------------------------------------------------------------- 1. data
df = load_data()
CITIES = sorted(df["city"].unique())
DEVICES = sorted(df["device"].unique())

# ---------------------------------------------------------------- 2. app
app = Dash(
    __name__,
    external_stylesheets=[
        getattr(dbc.themes, THEME.bootstrap_theme),
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap",
    ],
    title=THEME.title,
)
server = app.server  # <- Render (gunicorn) needs this line!

# ---------------------------------------------------------------- 3. layout
header = html.Div([
    html.H1(THEME.title, className="app-title"),
    html.P(f"{THEME.subtitle} · {df['date'].min():%d %b %Y} – {df['date'].max():%d %b %Y}",
           className="app-subtitle"),
], className="app-header")

filters = dbc.Card(dbc.CardBody([
    html.H5("Filters", className="mb-3"),

    html.Label("Cities"),
    dcc.Dropdown(id="city-filter", options=CITIES, value=CITIES, multi=True,
                 className="mb-3"),

    html.Label("Devices"),
    dbc.Checklist(id="device-filter", options=DEVICES, value=DEVICES,
                  switch=True, className="mb-3"),

    html.Label("Period"),
    dcc.DatePickerRange(id="date-filter",
                        start_date=df["date"].min(), end_date=df["date"].max(),
                        min_date_allowed=df["date"].min(), max_date_allowed=df["date"].max(),
                        display_format="DD MMM YY", className="mb-3"),

    html.Label("Metric", className="d-block"),
    dbc.RadioItems(id="metric-filter",
                   options=[{"label": label, "value": col} for col, label in METRICS.items()],
                   value="steps"),
]), className="filter-card")


def graph_card(graph_id):
    """A card that holds one graph (a function, so we don't repeat ourselves)."""
    return dbc.Card(dcc.Graph(id=graph_id, config={"displayModeBar": False}),
                    className="graph-card")


app.layout = dbc.Container([
    header,
    dbc.Row([
        dbc.Col(filters, lg=3, className="mb-4"),
        dbc.Col([
            dbc.Row(id="kpi-row", className="g-3 mb-3"),
            dbc.Row([dbc.Col(graph_card("time-graph"), lg=6),
                     dbc.Col(graph_card("device-graph"), lg=6)], className="g-3 mb-3"),
            dbc.Row([dbc.Col(graph_card("scatter-graph"), lg=6),
                     dbc.Col(graph_card("map-graph"), lg=6)], className="g-3"),
        ], lg=9),
    ]),
    html.Footer("Built with Plotly Dash · Ironhack DSML", className="app-footer"),
], fluid=True)


# ---------------------------------------------------------------- 4. callback
@app.callback(
    Output("kpi-row", "children"),
    Output("time-graph", "figure"),
    Output("device-graph", "figure"),
    Output("scatter-graph", "figure"),
    Output("map-graph", "figure"),
    Input("city-filter", "value"),
    Input("device-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
    Input("metric-filter", "value"),
)
def update_dashboard(cities, devices, start_date, end_date, metric):
    """Runs every time a filter changes: filter the data, rebuild KPIs and figures."""
    filtered = filter_data(df, cities, devices, start_date, end_date)

    if filtered.empty:
        empty = charts.empty_figure()
        return [], empty, empty, empty, empty

    kpi_cards = [dbc.Col(card.render(), md=3) for card in build_kpis(filtered)]
    return (
        kpi_cards,
        charts.metric_over_time(filtered, metric),
        charts.metric_by_device(filtered, metric),
        charts.steps_vs_sleep(filtered),
        charts.city_map(filtered, metric),
    )


# ---------------------------------------------------------------- 5. run
if __name__ == "__main__":
    app.run(debug=True)