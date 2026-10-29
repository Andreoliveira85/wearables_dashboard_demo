# Wearable Health Monitor

An interactive dashboard built with **Plotly Dash**. It shows sleep, activity and heart-rate data from 250 users across 8 European cities, from Oct 2025 to Sep 2026.

You can filter by city, device and period, and pick the metric to display. Four KPI cards and four charts update instantly.

---

## Quick start

You need **Python 3.12** (we use 3.12.13 through pyenv).

```bash
# 1. go into the project folder
cd wearables_dashboard_demo

# 2. use the right Python version (creates/uses .python-version)
pyenv local 3.12.13
python3.12 --version          # -> Python 3.12.13

# 3. create the virtual environment
python3.12 -m venv .venv

# 4. (optional) fix the "((.venv) )" prompt bug of Python 3.12 -> shows "(venv)"
sed -i '' 's|PS1="(".*|PS1="(venv) ${PS1:-}"|' .venv/bin/activate

# 5. activate it (do this every time you open a new terminal)
source .venv/bin/activate

# 6. install the packages
python -m pip install --upgrade pip
pip install -r requirements.txt

# 7. run the dashboard
python app.py
```

Then open **http://127.0.0.1:8050** in your browser. Stop the app with `Ctrl + C`.

### For the notebooks
The notebooks need a few extra packages:

```bash
pip install ipykernel nbformat statsmodels
```

In VS Code, pick the **`.venv` (Python 3.12.13)** kernel in the top right of the notebook.

---

## Project structure

```
wearables_dashboard_demo/
├── app.py              # the dashboard: layout (what we see) + callback (what happens on click)
├── config.py           # look & settings: title, theme, colours, metrics  <- customise here
├── data.py             # load the CSV and filter it
├── charts.py           # one function per chart, each returns a Plotly figure
├── kpis.py             # KpiCard class: the big numbers at the top
├── explore.py          # first script: prints a quick summary of the data
├── assets/
│   └── style.css       # custom CSS, loaded automatically by Dash
├── data/
│   └── wearables_daily.csv
├── notebooks/
│   ├── W03_D2_plotly_eda.ipynb        # exploratory analysis with Plotly
│   └── W03_D2_plotly_eda_live.ipynb   # live-coding version for class
├── style_original.css  # backup of the calmer CSS (not loaded by Dash)
└── requirements.txt
```

**One file, one job.** `app.py` only puts the pieces together; the work happens in the other files.

### Test each file on its own
Every module has a small test in its `if __name__ == "__main__":` block:

| Command | What it does |
|---|---|
| `python explore.py` | prints rows, users, date range, devices and cities |
| `python data.py` | loads the data and shows a filtered sample |
| `python charts.py` | opens one chart in the browser |
| `python kpis.py` | prints one formatted KPI value |

---

## The data

`data/wearables_daily.csv`: **one row = one user on one day** (91,250 rows).

| Column | Meaning |
|---|---|
| `user_id`, `age`, `age_group`, `gender` | who |
| `date`, `city`, `lat`, `lon`, `device` | when, where, which wearable |
| `steps`, `active_minutes`, `calories` | activity |
| `sleep_hours`, `deep_sleep_pct` | sleep |
| `resting_hr`, `hrv_ms`, `stress_score` | heart & stress |

Data notes (found during the EDA):
- Days with **≥ 50,000 steps** are sensor glitches. `load_data()` removes them.
- **Withings is missing ~40 % of its HRV values**; the other devices miss none.
- Withings users are on average ~5 years younger, so watch out for this when you compare devices.

---

## Customise your dashboard

Most changes need **only `config.py`**:

| Setting | Example |
|---|---|
| `title`, `subtitle` | your dashboard's name |
| `accent_color` | `"#FF6B8B"`: KPI numbers and line colour |
| `palette` | colours used for devices and age groups |
| `METRICS` | which metrics appear in the radio buttons |

For the look of the page (background, cards, hover effects), edit **`assets/style.css`**. Save, and the browser reloads by itself.

> ⚠️ **Theme rule:** three things must agree: `bootstrap_theme`, `plotly_template` and the background in `style.css`.
> The CSS uses a dark background, so keep a **dark** theme (`CYBORG`, `DARKLY`, `SLATE`, `VAPOR`, `SUPERHERO`) with `plotly_template = "plotly_dark"`.
> Light themes (`FLATLY`, `MINTY`, `LUX`) also need `style.css` changed; otherwise the text becomes unreadable.

To go back to the calmer original style: `cp style_original.css assets/style.css`

---

## Troubleshooting

| Problem | Cause → fix |
|---|---|
| `python3.12: command not found` | pyenv isn't using 3.12 in this folder → `pyenv local 3.12.13`. Don't reinstall it (answer **N** if pyenv asks). |
| Prompt shows `((.venv) )` | bug in Python 3.12's activate script → step 4 of the Quick start |
| `ValueError: Mime type rendering requires nbformat>=4.2.0` | the notebook runs a different Python → select the `.venv` kernel. Check with `import sys; print(sys.executable)`; it must end in `.venv/bin/python`. Then `%pip install nbformat` and restart the kernel. |
| `SyntaxError` on a line with only ```` ``` ```` | Markdown backticks were copied with the code → delete that line |
| `python charts.py` shows an invisible title/axes | the figures have a transparent background (made for the dark dashboard), and the test page is white. This only affects the quick test, not the app. |
| CSS changes don't appear | hard refresh with **Cmd + Shift + R** |
| Port 8050 already in use | an old app is still running → stop it with `Ctrl + C` in its terminal |

---

## Deploy (Render)

`app.py` already exposes `server = app.server`, which is what gunicorn needs.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:server`

---

Built with Plotly Dash · Ironhack DSML
