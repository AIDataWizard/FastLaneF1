import pandas as pd
import plotly.express as px

# --- Load laps data ---
laps = pd.read_csv("data/2024_Brazil_Race/laps.csv")

# --- Focus on a few drivers ---
drivers = ["VER", "NOR"]
laps = laps[laps["Driver"].isin(drivers)]

# --- Convert LapTime to seconds ---
laps["LapTimeSeconds"] = (
    pd.to_timedelta(laps["LapTime"]).dt.total_seconds()
)

# --- Compute average lap time per driver ---
avg_lap = laps.groupby("Driver")["LapTimeSeconds"].mean().reset_index()
print("🏎️  Average lap times (seconds):")
print(avg_lap)

# --- Plot lap-by-lap comparison ---
fig = px.line(
    laps,
    x="LapNumber",
    y="LapTimeSeconds",
    color="Driver",
    title="Lap-by-Lap Race Pace – Brazil 2024",
    markers=True,
)
fig.update_layout(xaxis_title="Lap Number", yaxis_title="Lap Time (s)")
fig.show()
