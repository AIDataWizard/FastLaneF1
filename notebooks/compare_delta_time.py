import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Load telemetry data for both drivers ---
ver = pd.read_csv("data/2024_Brazil_Race/VER_telemetry.csv")
nor = pd.read_csv("data/2024_Brazil_Race/NOR_telemetry.csv")

# --- Basic cleanup ---
ver = ver.dropna(subset=["Distance", "Speed", "Time"])
nor = nor.dropna(subset=["Distance", "Speed", "Time"])

# --- Convert Time column to seconds ---
def to_seconds(time_series):
    return pd.to_timedelta(time_series).dt.total_seconds()

ver["TimeSeconds"] = to_seconds(ver["Time"])
nor["TimeSeconds"] = to_seconds(nor["Time"])

# --- Align both drivers to a common Distance scale ---
common_distance = np.linspace(
    min(ver["Distance"].min(), nor["Distance"].min()),
    max(ver["Distance"].max(), nor["Distance"].max()),
    2000
)

# --- Interpolate cumulative time (in seconds) for each driver ---
ver_time = np.interp(common_distance, ver["Distance"], ver["TimeSeconds"])
nor_time = np.interp(common_distance, nor["Distance"], nor["TimeSeconds"])

# --- Compute delta (Norris - Verstappen) ---
delta = nor_time - ver_time

# --- Create DataFrame for plotting ---
delta_df = pd.DataFrame({
    "Distance": common_distance,
    "DeltaTime": delta
})

# --- Plot the Delta chart ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=delta_df["Distance"],
    y=delta_df["DeltaTime"],
    mode="lines",
    line=dict(width=2, color="orange"),
    name="Δ Time (Norris - Verstappen)"
))

# --- Add zero reference line ---
fig.add_hline(y=0, line=dict(color="white", width=1, dash="dash"))

fig.update_layout(
    title="Delta Time vs Distance – Brazil GP 2024 (Fastest Lap)",
    xaxis_title="Distance (m)",
    yaxis_title="Δ Time (s)",
    template="plotly_dark",
    hovermode="x unified",
    showlegend=True
)

fig.show()
