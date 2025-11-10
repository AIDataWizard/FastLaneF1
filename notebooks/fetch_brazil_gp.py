import fastf1
from fastf1 import plotting
import pandas as pd
import os

# Enable FastF1 cache (it saves downloaded data locally)
fastf1.Cache.enable_cache('data/cache')

# --- Choose race details ---
YEAR = 2024
GRAND_PRIX = 'Brazil'
SESSION = 'R'   # 'R' = Race, 'Q' = Quali, 'FP1' = Practice 1

# --- Load the session ---
print(f"🔄 Loading {GRAND_PRIX} {YEAR} {SESSION} data...")
session = fastf1.get_session(YEAR, GRAND_PRIX, SESSION)
session.load(laps=True, telemetry=True, weather=True)
print("✅ Session loaded successfully!")

# --- Create output folder ---
output_dir = f"data/{YEAR}_{GRAND_PRIX}_Race"
os.makedirs(output_dir, exist_ok=True)

# --- Save laps data ---
laps_df = session.laps
laps_path = f"{output_dir}/laps.csv"
laps_df.to_csv(laps_path, index=False)
print(f"📄 Saved laps data to {laps_path}")

# --- Save weather data ---
weather_df = session.weather_data
weather_path = f"{output_dir}/weather.csv"
weather_df.to_csv(weather_path, index=False)
print(f"🌤 Saved weather data to {weather_path}")

# --- Save telemetry for a few sample drivers ---
drivers = ['VER', 'NOR', 'LEC']  # Verstappen, Norris, Leclerc
for driver in drivers:
    print(f"📈 Processing telemetry for {driver}...")
    drv_laps = laps_df.pick_driver(driver)
    fastest_lap = drv_laps.pick_fastest()
    telemetry = fastest_lap.get_car_data().add_distance()
    telemetry_path = f"{output_dir}/{driver}_telemetry.csv"
    telemetry.to_csv(telemetry_path, index=False)
    print(f"💾 Saved telemetry for {driver} to {telemetry_path}")

print("\n🏁 All data downloaded and saved successfully!")
