import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="FastLaneF1 Dashboard", layout="wide")
st.title("🏎️ FastLaneF1 – Formula 1 Telemetry & Lap Analysis")

# --- Sidebar inputs ---
st.sidebar.header("Select Options")
year = st.sidebar.selectbox("Select Year", [2024])
race = st.sidebar.selectbox("Select Race", ["Brazil"])
drivers = st.sidebar.multiselect(
    "Select Drivers", ["VER", "NOR", "LEC"], default=["VER", "NOR"]
)

# --- Load laps data ---
laps_path = f"data/{year}_{race}_Race/laps.csv"
laps = pd.read_csv(laps_path)
laps = laps[laps["Driver"].isin(drivers)]
laps["LapTimeSeconds"] = pd.to_timedelta(laps["LapTime"]).dt.total_seconds()

# --- Lap time comparison ---
fig1 = px.line(
    laps, x="LapNumber", y="LapTimeSeconds", color="Driver",
    title=f"Lap-by-Lap Race Pace – {race} {year}", markers=True
)
fig1.update_layout(xaxis_title="Lap Number", yaxis_title="Lap Time (s)")

# --- Telemetry comparison (Speed vs Distance) ---
telemetry = []
for d in drivers:
    df = pd.read_csv(f"data/{year}_{race}_Race/{d}_telemetry.csv")
    df["Driver"] = d
    telemetry.append(df)
telemetry = pd.concat(telemetry)
telemetry = telemetry.dropna(subset=["Speed", "Distance"])

fig2 = px.line(
    telemetry, x="Distance", y="Speed", color="Driver",
    title=f"Speed vs Distance – {race} {year}"
)
fig2.update_layout(xaxis_title="Distance (m)", yaxis_title="Speed (km/h)")

# --- Delta-time chart (if two drivers selected) ---
if len(drivers) == 2:
    ver = telemetry[telemetry["Driver"] == drivers[0]].copy()
    nor = telemetry[telemetry["Driver"] == drivers[1]].copy()
    ver["TimeSeconds"] = pd.to_timedelta(ver["Time"]).dt.total_seconds()
    nor["TimeSeconds"] = pd.to_timedelta(nor["Time"]).dt.total_seconds()

    common_distance = np.linspace(
        min(ver["Distance"].min(), nor["Distance"].min()),
        max(ver["Distance"].max(), nor["Distance"].max()),
        2000,
    )
    ver_time = np.interp(common_distance, ver["Distance"], ver["TimeSeconds"])
    nor_time = np.interp(common_distance, nor["Distance"], nor["TimeSeconds"])
    delta = nor_time - ver_time

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=common_distance, y=delta, mode="lines",
        line=dict(width=2, color="orange"),
        name=f"Δ Time ({drivers[1]} – {drivers[0]})"
    ))
    fig3.add_hline(y=0, line=dict(color="white", width=1, dash="dash"))
    fig3.update_layout(
        title=f"Delta Time vs Distance – {race} {year}",
        xaxis_title="Distance (m)",
        yaxis_title="Δ Time (s)",
        template="plotly_dark",
        hovermode="x unified"
    )
else:
    fig3 = None

# --- Display charts in layout ---
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
if fig3:
    st.plotly_chart(fig3, use_container_width=True)
