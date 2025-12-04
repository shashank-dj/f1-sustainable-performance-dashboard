import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========== PATH CONFIGURATION ==========
BASE_PATH = "formula-1-dataset-race-data-and-telemetry/Directories/LapData"

# ========== LOAD AVAILABLE RACES ==========
def list_races():
    files = os.listdir(BASE_PATH)
    race_files = [f for f in files if f.endswith(".csv")]
    race_names = [f.replace("_", " ").replace(".csv", "") for f in race_files]
    return race_files, race_names

race_files, race_names = list_races()

# ========== DATA LOADING ==========
@st.cache_data
def load_data(selected_file):
    df = pd.read_csv(os.path.join(BASE_PATH, selected_file))
    return df

st.sidebar.header("Race Selection")
selected_race_name = st.sidebar.selectbox("Select Race", race_names)
selected_race_file = race_files[race_names.index(selected_race_name)]

df = load_data(selected_race_file)

# ========== FEATURE ENGINEERING ==========
def prepare_features(df):
    df = df.copy()
    df["SectorTotal"] = df["Sector1Time"] + df["Sector2Time"] + df["Sector3Time"]
    df["LapTimeDelta"] = df.groupby("Driver")["LapTime"].diff()

    threshold = df["LapTime"].mean() + 3 * df["LapTime"].std()
    df["IsPitStop"] = df["LapTime"] > threshold

    df["Stint"] = df.groupby("Driver")["IsPitStop"].cumsum() + 1
    df["DegradationRate"] = df["LapTimeDelta"] / df["TyreLife"]
    return df

df = prepare_features(df)

# ========== DRIVER SELECTION ==========
driver_options = sorted(df["Driver"].unique())

st.sidebar.header("Driver Selection")
driver1 = st.sidebar.selectbox("Select Driver 1", driver_options)
driver2 = st.sidebar.selectbox("Select Driver 2", driver_options, index=1)

show_degradation = st.sidebar.checkbox("Show Degradation Rate", value=True)
show_pitstops = st.sidebar.checkbox("Highlight Pit Stops", value=True)

d1 = df[df["Driver"] == driver1]
d2 = df[df["Driver"] == driver2]

# ========== SUSTAINABILITY SCORE ==========
def calculate_sustainability_score(df, driver):
    df_driver = df[df["Driver"] == driver].copy()

    stint_lengths = df_driver.groupby("Stint")["LapNumber"].count()
    avg_stint_length = stint_lengths.mean()

    valid_degradation = df_driver["DegradationRate"].replace([float("inf"), float("-inf")], pd.NA).dropna()
    degr_rate_mean = valid_degradation.mean() if len(valid_degradation) > 0 else 0

    avg_lap_time = df_driver["LapTime"].mean()
    pit_lap_times = df_driver[df_driver["IsPitStop"]]["LapTime"]
    pit_loss_time = (pit_lap_times - avg_lap_time).mean() if len(pit_lap_times) > 0 else 0

    score = (avg_stint_length / abs(degr_rate_mean)) - pit_loss_time if degr_rate_mean != 0 else 0

    return {
        "Driver": driver,
        "AvgStintLength": avg_stint_length,
        "DegradationRateMean": degr_rate_mean,
        "PitStopLossTime": pit_loss_time,
        "SustainabilityScore": score
    }

# ========== DASHBOARD UI ==========
st.title("Sustainable Performance Optimization in Formula 1 🌱🏎️")
st.write(f"Interactive dashboard analyzing telemetry & sustainability performance for **{selected_race_name}**.")

# -------- Lap Time Comparison --------
st.subheader("Lap Time Comparison")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(d1["LapNumber"], d1["LapTime"], marker="o", label=driver1)
ax.plot(d2["LapNumber"], d2["LapTime"], marker="o", label=driver2)

if show_pitstops:
    pit1 = d1[d1["IsPitStop"]]
    pit2 = d2[d2["IsPitStop"]]
    ax.scatter(pit1["LapNumber"], pit1["LapTime"], color="red", label=f"{driver1} Pit")
    ax.scatter(pit2["LapNumber"], pit2["LapTime"], color="purple", label=f"{driver2} Pit")

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time (s)")
ax.set_title(f"Lap Time vs Laps: {driver1} vs {driver2}")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# -------- Degradation Comparison --------
if show_degradation:
    st.subheader("Degradation Rate Comparison")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(d1["LapNumber"], d1["DegradationRate"], marker="o", label=driver1)
    ax2.plot(d2["LapNumber"], d2["DegradationRate"], marker="o", label=driver2)
    ax2.axhline(0, color="gray", linestyle="--")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

# -------- Sustainability Score --------
st.subheader("Sustainability Score Comparison")

score1 = calculate_sustainability_score(df, driver1)
score2 = calculate_sustainability_score(df, driver2)

score_df = pd.DataFrame([score1, score2])
st.dataframe(score_df)

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.bar(score_df["Driver"], score_df["SustainabilityScore"])
ax3.set_title("Sustainability Score Comparison")
ax3.set_ylabel("Score")
ax3.grid(axis="y", linestyle="--")
st.pyplot(fig3)

# -------- Final Conclusion --------
if score1["SustainabilityScore"] > score2["SustainabilityScore"]:
    st.success(f"### 🚀 Conclusion\n**{driver1} demonstrates a higher sustainability performance score than {driver2}.**\nThis indicates more efficient tyre management, better stint stability, and minimized pit stop time loss.")
elif score2["SustainabilityScore"] > score1["SustainabilityScore"]:
    st.success(f"### 🚀 Conclusion\n**{driver2} demonstrates a higher sustainability performance score than {driver1}.**\nThis reflects stronger resource-efficient driving strategy and better tyre degradation control across the race.")
else:
    st.info(f"### ⚖ Balanced Performance\nBoth {driver1} and {driver2} achieved identical sustainability scores, indicating comparable efficiency in strategy execution and tyre usage.")

st.write("Higher score = stronger sustainability efficiency 🌱")
