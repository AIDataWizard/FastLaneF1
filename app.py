# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# # import numpy as np

# # st.set_page_config(page_title="FastLaneF1 Dashboard", layout="wide")
# # st.title("🏎️ FastLaneF1 – Formula 1 Telemetry & Lap Analysis")

# # # --- Sidebar inputs ---
# # st.sidebar.header("Select Options")
# # year = st.sidebar.selectbox("Select Year", [2024])
# # race = st.sidebar.selectbox("Select Race", ["Brazil"])
# # drivers = st.sidebar.multiselect(
# #     "Select Drivers", ["VER", "NOR", "LEC"], default=["VER", "NOR"]
# # )

# # # --- Load laps data ---
# # laps_path = f"data/{year}_{race}_Race/laps.csv"
# # laps = pd.read_csv(laps_path)
# # laps = laps[laps["Driver"].isin(drivers)]
# # laps["LapTimeSeconds"] = pd.to_timedelta(laps["LapTime"]).dt.total_seconds()

# # # --- Lap time comparison ---
# # fig1 = px.line(
# #     laps, x="LapNumber", y="LapTimeSeconds", color="Driver",
# #     title=f"Lap-by-Lap Race Pace – {race} {year}", markers=True
# # )
# # fig1.update_layout(xaxis_title="Lap Number", yaxis_title="Lap Time (s)")

# # # --- Telemetry comparison (Speed vs Distance) ---
# # telemetry = []
# # for d in drivers:
# #     df = pd.read_csv(f"data/{year}_{race}_Race/{d}_telemetry.csv")
# #     df["Driver"] = d
# #     telemetry.append(df)
# # telemetry = pd.concat(telemetry)
# # telemetry = telemetry.dropna(subset=["Speed", "Distance"])

# # fig2 = px.line(
# #     telemetry, x="Distance", y="Speed", color="Driver",
# #     title=f"Speed vs Distance – {race} {year}"
# # )
# # fig2.update_layout(xaxis_title="Distance (m)", yaxis_title="Speed (km/h)")

# # # --- Delta-time chart (if two drivers selected) ---
# # if len(drivers) == 2:
# #     ver = telemetry[telemetry["Driver"] == drivers[0]].copy()
# #     nor = telemetry[telemetry["Driver"] == drivers[1]].copy()
# #     ver["TimeSeconds"] = pd.to_timedelta(ver["Time"]).dt.total_seconds()
# #     nor["TimeSeconds"] = pd.to_timedelta(nor["Time"]).dt.total_seconds()

# #     common_distance = np.linspace(
# #         min(ver["Distance"].min(), nor["Distance"].min()),
# #         max(ver["Distance"].max(), nor["Distance"].max()),
# #         2000,
# #     )
# #     ver_time = np.interp(common_distance, ver["Distance"], ver["TimeSeconds"])
# #     nor_time = np.interp(common_distance, nor["Distance"], nor["TimeSeconds"])
# #     delta = nor_time - ver_time

# #     fig3 = go.Figure()
# #     fig3.add_trace(go.Scatter(
# #         x=common_distance, y=delta, mode="lines",
# #         line=dict(width=2, color="orange"),
# #         name=f"Δ Time ({drivers[1]} – {drivers[0]})"
# #     ))
# #     fig3.add_hline(y=0, line=dict(color="white", width=1, dash="dash"))
# #     fig3.update_layout(
# #         title=f"Delta Time vs Distance – {race} {year}",
# #         xaxis_title="Distance (m)",
# #         yaxis_title="Δ Time (s)",
# #         template="plotly_dark",
# #         hovermode="x unified"
# #     )
# # else:
# #     fig3 = None

# # # --- Display charts in layout ---
# # st.plotly_chart(fig1, use_container_width=True)
# # st.plotly_chart(fig2, use_container_width=True)
# # if fig3:
# #     st.plotly_chart(fig3, use_container_width=True)


# # Updated Code for dynamic style fetching 
# # Dynamic FastF1 data fetching
# # ✅ Lap-time comparison
# # ✅ Speed vs Distance telemetry
# # ✅ Delta-time graph
# # ✅ Clean Streamlit UI
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import fastf1
# from fastf1 import plotting
# import warnings
# warnings.filterwarnings("ignore")

# # ---------------------------------------------
# # PAGE CONFIG
# # ---------------------------------------------
# st.set_page_config(page_title="FastLaneF1 Analytics", layout="wide")
# st.title("🏎️ FastLaneF1 – Live F1 Telemetry & Race Analytics")

# # Enable cache (stored temporarily on Render)
# import os
# os.makedirs("cache", exist_ok=True)
# fastf1.Cache.enable_cache("cache")

# # ---------------------------------------------
# # CACHED DATA LOADER
# # ---------------------------------------------
# @st.cache_data(show_spinner=False)
# def load_f1_session(year, gp, session_type):
#     """Fetch and cache F1 session data from FastF1"""
#     session = fastf1.get_session(year, gp, session_type)
#     session.load()
#     return session

# # ---------------------------------------------
# # SIDEBAR INPUTS
# # ---------------------------------------------
# st.sidebar.header("Session Selection")

# year = st.sidebar.selectbox("Year", [2021, 2022, 2023, 2024])

# gp = st.sidebar.selectbox(
#     "Grand Prix",
#     [
#         "Bahrain", "Saudi Arabia", "Australia", "Azerbaijan", "Miami", "Monaco",
#         "Spain", "Canada", "Austria", "Great Britain", "Hungary", "Belgium",
#         "Netherlands", "Italy", "Singapore", "Japan", "Qatar", "United States",
#         "Mexico", "Brazil", "Las Vegas", "Abu Dhabi",
#     ],
#     index=8  # Default = Austria for faster startup
# )

# session_type = st.sidebar.selectbox("Session", ["Race", "Qualifying", "Sprint"])
# drivers = st.sidebar.multiselect("Drivers", ["VER", "NOR", "HAM", "LEC", "PER", "SAI"], default=["VER", "NOR"])

# st.sidebar.write("---")

# # ---------------------------------------------
# # LOAD FASTF1 SESSION WITH "FAST MODE" OPTION
# # ---------------------------------------------
# light_mode = st.sidebar.checkbox("🕹️ Fast Mode (skip telemetry)", value=True)

# st.write(f"### Loading {session_type} data for {gp} {year}... ⏳")

# try:
#     if light_mode:
#         with st.spinner(f"⚡ Loading {gp} {session_type} summary (no telemetry)..."):
#             session = fastf1.get_session(year, gp, session_type)
#             # Load only laps + timing info (no car telemetry)
#             session.load(laps=True, telemetry=False)
#         st.success(f"✅ Loaded summary for {gp} {session_type} ({year})")
#     else:
#         with st.spinner(f"🔄 Fetching full telemetry for {gp} {session_type} ({year})... this may take a minute ⏱️"):
#             session = load_f1_session(year, gp, session_type)
#         st.success(f"✅ Loaded full data for {gp} {session_type} ({year})")
# except Exception as e:
#     st.error(f"❌ Could not load session data: {e}")
#     st.stop()

# # ---------------------------------------------
# # LAP TIME COMPARISON
# # ---------------------------------------------
# laps = session.laps.pick_drivers(drivers)
# laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

# fig1 = px.line(
#     laps,
#     x="LapNumber",
#     y="LapTimeSeconds",
#     color="Driver",
#     title=f"Lap-by-Lap Pace – {gp} {year} ({session_type})",
#     markers=True,
# )
# fig1.update_layout(xaxis_title="Lap Number", yaxis_title="Lap Time (s)", template="plotly_dark")
# st.plotly_chart(fig1, width="stretch")

# # ---------------------------------------------
# # TELEMETRY COMPARISON (FASTEST LAP)
# # ---------------------------------------------
# telemetry = pd.DataFrame()
# for drv in drivers:
#     try:
#         fastest_lap = laps.pick_driver(drv).pick_fastest()
#         drv_tel = fastest_lap.get_car_data().add_distance()
#         drv_tel["Driver"] = drv
#         telemetry = pd.concat([telemetry, drv_tel])
#     except Exception:
#         st.warning(f"⚠️ No telemetry data available for {drv}")

# if not telemetry.empty:
#     fig2 = px.line(
#         telemetry,
#         x="Distance",
#         y="Speed",
#         color="Driver",
#         title=f"Speed vs Distance – Fastest Lap ({gp} {year})",
#     )
#     fig2.update_layout(xaxis_title="Distance (m)", yaxis_title="Speed (km/h)", template="plotly_dark")
#     st.plotly_chart(fig2, width="stretch")
# else:
#     st.warning("⚠️ No telemetry data available for selected drivers.")

# # ---------------------------------------------
# # DELTA-TIME COMPARISON
# # ---------------------------------------------
# if len(drivers) == 2:
#     d1, d2 = drivers
#     st.write(f"### Delta-Time Analysis: {d2} vs {d1}")

#     tel1 = telemetry[telemetry["Driver"] == d1]
#     tel2 = telemetry[telemetry["Driver"] == d2]

#     if not tel1.empty and not tel2.empty:
#         common_dist = np.linspace(
#             min(tel1["Distance"].min(), tel2["Distance"].min()),
#             max(tel1["Distance"].max(), tel2["Distance"].max()),
#             2000,
#         )

#         def to_seconds(df):
#             return df["Time"].dt.total_seconds()

#         t1 = np.interp(common_dist, tel1["Distance"], to_seconds(tel1))
#         t2 = np.interp(common_dist, tel2["Distance"], to_seconds(tel2))

#         delta = t2 - t1
#         fig3 = go.Figure()
#         fig3.add_trace(
#             go.Scatter(
#                 x=common_dist,
#                 y=delta,
#                 mode="lines",
#                 name=f"Δ Time ({d2} - {d1})",
#                 line=dict(width=2, color="orange"),
#             )
#         )
#         fig3.add_hline(y=0, line=dict(color="white", width=1, dash="dash"))
#         fig3.update_layout(
#             title=f"Delta Time vs Distance – {gp} {year}",
#             xaxis_title="Distance (m)",
#             yaxis_title="Δ Time (s)",
#             template="plotly_dark",
#             hovermode="x unified",
#         )
#         st.plotly_chart(fig3, width="stretch")
#     else:
#         st.warning("⚠️ Delta comparison not possible (missing telemetry).")
# else:
#     st.info("ℹ️ Select exactly two drivers for delta-time comparison.")

# # ---------------------------------------------
# # FOOTER
# # ---------------------------------------------
# st.write("---")
# st.markdown(
#     "Built with ❤️ by **WeAreChecking** | Powered by [FastF1](https://docs.fastf1.dev/) and Streamlit 🚀"
# )



# ⚙️ What This Version Does

# ✅ Handles Render limitations automatically
# ✅ Retries on network hiccups
# ✅ Caches data for 30 min (no repeat fetch)
# ✅ Prevents memory overload (400 MB limit)
# ✅ Spinner feedback during heavy loads
# ✅ Fast Mode default = instant load

import os
import time
import resource
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fastf1
from fastf1 import plotting

# ---------------------------------------------
# BASIC CONFIG & MEMORY LIMIT
# ---------------------------------------------
st.set_page_config(page_title="FastLaneF1 Analytics", layout="wide")
st.title("🏎️ FastLaneF1 – Live F1 Telemetry & Race Analytics")

# Prevent Render from killing process due to over-memory usage
try:
    resource.setrlimit(resource.RLIMIT_AS, (400 * 1024 * 1024, -1))
except Exception:
    pass  # not supported on all systems

# Create cache directory if missing
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

# ---------------------------------------------
# CACHED DATA LOADERS
# ---------------------------------------------
@st.cache_data(show_spinner=False, ttl=1800)
def load_f1_session(year, gp, session_type):
    """Fetch and cache a full F1 session with retry logic."""
    session = fastf1.get_session(year, gp, session_type)
    for attempt in range(3):
        try:
            session.load()
            return session
        except Exception as e:
            if attempt < 2:
                st.warning(f"⚠️ Attempt {attempt+1} failed: {e}. Retrying...")
                time.sleep(3)
            else:
                raise e

@st.cache_data(show_spinner=False, ttl=1800)
def load_f1_summary(year, gp, session_type):
    """Fetch and cache a lightweight session summary (laps only)."""
    session = fastf1.get_session(year, gp, session_type)
    session.load(laps=True, telemetry=False)
    return session

# ---------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------
st.sidebar.header("Session Selection")

year = st.sidebar.selectbox("Year", [2021, 2022, 2023, 2024])

gp = st.sidebar.selectbox(
    "Grand Prix",
    [
        "Bahrain", "Saudi Arabia", "Australia", "Azerbaijan", "Miami", "Monaco",
        "Spain", "Canada", "Austria", "Great Britain", "Hungary", "Belgium",
        "Netherlands", "Italy", "Singapore", "Japan", "Qatar", "United States",
        "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"
    ],
    index=8  # Austria = lighter dataset
)

session_type = st.sidebar.selectbox("Session", ["Race", "Qualifying", "Sprint"])
drivers = st.sidebar.multiselect("Drivers", ["VER", "NOR", "HAM", "LEC", "PER", "SAI"], default=["VER", "NOR"])
light_mode = st.sidebar.checkbox("🕹️ Fast Mode (skip telemetry)", value=True)
st.sidebar.write("---")

# ---------------------------------------------
# LOAD SESSION (FAST OR FULL)
# ---------------------------------------------
st.write(f"### Loading {session_type} data for {gp} {year}... ⏳")

try:
    if light_mode:
        with st.spinner(f"⚡ Loading {gp} {session_type} summary (no telemetry)..."):
            session = load_f1_summary(year, gp, session_type)
        st.success(f"✅ Loaded summary for {gp} {session_type} ({year})")
    else:
        with st.spinner(f"🔄 Fetching full telemetry for {gp} {session_type} ({year})... this may take a minute ⏱️"):
            session = load_f1_session(year, gp, session_type)
        st.success(f"✅ Loaded full data for {gp} {session_type} ({year})")
except Exception as e:
    st.error(f"❌ Could not load session data: {e}")
    st.stop()

# ---------------------------------------------
# PLOT 1 — LAP TIME COMPARISON
# ---------------------------------------------
laps = session.laps.pick_drivers(drivers)
laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

fig1 = px.line(
    laps, x="LapNumber", y="LapTimeSeconds", color="Driver",
    title=f"Lap-by-Lap Pace – {gp} {year} ({session_type})", markers=True
)
fig1.update_layout(xaxis_title="Lap", yaxis_title="Lap Time (s)", template="plotly_dark")
st.plotly_chart(fig1, width="stretch")

# ---------------------------------------------
# PLOT 2 — TELEMETRY COMPARISON (FULL MODE)
# ---------------------------------------------
if light_mode:
    st.info("🕹️ Fast Mode active — showing only lap time analysis (telemetry skipped).")
else:
    telemetry = pd.DataFrame()
    for drv in drivers:
        try:
            fastest = laps.pick_driver(drv).pick_fastest()
            drv_tel = fastest.get_car_data().add_distance()
            drv_tel["Driver"] = drv
            telemetry = pd.concat([telemetry, drv_tel])
        except Exception:
            st.warning(f"⚠️ Some telemetry missing for {drv}")

    # Only display charts if telemetry exists
    if not telemetry.empty:
        # Speed vs Distance chart
        fig2 = px.line(
            telemetry, x="Distance", y="Speed", color="Driver",
            title=f"Speed vs Distance – Fastest Lap ({gp} {year})"
        )
        fig2.update_layout(
            xaxis_title="Distance (m)",
            yaxis_title="Speed (km/h)",
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white")
        )
        st.plotly_chart(fig2, width="stretch")

        # Delta chart only if 2 drivers selected
        if len(drivers) == 2:
            d1, d2 = drivers
            st.write(f"### Delta-Time Analysis: {d2} vs {d1}")
            tel1 = telemetry[telemetry["Driver"] == d1]
            tel2 = telemetry[telemetry["Driver"] == d2]
            if not tel1.empty and not tel2.empty:
                common_dist = np.linspace(
                    min(tel1["Distance"].min(), tel2["Distance"].min()),
                    max(tel1["Distance"].max(), tel2["Distance"].max()),
                    2000
                )
                t1 = np.interp(common_dist, tel1["Distance"], tel1["Time"].dt.total_seconds())
                t2 = np.interp(common_dist, tel2["Distance"], tel2["Time"].dt.total_seconds())
                delta = t2 - t1
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=common_dist, y=delta, mode="lines",
                    name=f"Δ Time ({d2} - {d1})",
                    line=dict(width=2, color="orange")
                ))
                fig3.add_hline(y=0, line=dict(color="white", width=1, dash="dash"))
                fig3.update_layout(
                    title=f"Delta Time vs Distance – {gp} {year}",
                    xaxis_title="Distance (m)",
                    yaxis_title="Δ Time (s)",
                    template="plotly_dark",
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117",
                    font=dict(color="white"),
                    hovermode="x unified"
                )
                st.plotly_chart(fig3, width="stretch")
    else:
        st.info("ℹ️ Telemetry data not available for this session.")

# ---------------------------------------------
# FOOTER
# ---------------------------------------------
st.write("---")
st.markdown(
    "Built with ❤️ by **WeAreChecking** | Powered by [FastF1](https://docs.fastf1.dev/) and Streamlit 🚀"
)
