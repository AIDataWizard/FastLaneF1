import pandas as pd
import plotly.graph_objects as go

# --- Load telemetry data ---
ver = pd.read_csv("data/2024_Brazil_Race/VER_telemetry.csv")
nor = pd.read_csv("data/2024_Brazil_Race/NOR_telemetry.csv")

# --- Add driver labels ---
ver["Driver"] = "Verstappen"
nor["Driver"] = "Norris"

# --- Combine into one DataFrame ---
telemetry = pd.concat([ver, nor])

# --- Basic cleaning ---
# Sometimes FastF1 data includes NaN at start/end, drop them
telemetry = telemetry.dropna(subset=["Speed", "Distance"])

# --- Plot Speed vs Distance using Plotly ---
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ver["Distance"],
        y=ver["Speed"],
        mode="lines",
        name="Verstappen",
        line=dict(width=2, color="red"),
    )
)

fig.add_trace(
    go.Scatter(
        x=nor["Distance"],
        y=nor["Speed"],
        mode="lines",
        name="Norris",
        line=dict(width=2, color="blue"),
    )
)

fig.update_layout(
    title="Telemetry Comparison: Speed vs Distance – Brazil GP 2024 (Fastest Lap)",
    xaxis_title="Distance (m)",
    yaxis_title="Speed (km/h)",
    template="plotly_dark",
    hovermode="x unified",
)

fig.show()
