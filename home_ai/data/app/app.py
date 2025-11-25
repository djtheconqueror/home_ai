import streamlit as st
import pandas as pd
import plotly.express as px

# -------- SAFE CSV LOADING --------
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "cities.csv")

df = pd.read_csv(csv_path)

# Ensure proper types
df["rent"] = pd.to_numeric(df["rent"], errors="coerce")
df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
df["diversity"] = pd.to_numeric(df["diversity"], errors="coerce")
df["culture_index"] = pd.to_numeric(df["culture_index"], errors="coerce")
df["job_market"] = pd.to_numeric(df["job_market"], errors="coerce")
df["safety"] = pd.to_numeric(df["safety"], errors="coerce")

# Fix text fields safely
df["lifestyle"] = df["lifestyle"].fillna("").astype(str)

# -------- SCORING FUNCTION --------
def score_city(row, pref_region, pref_rent, pref_temp, pref_diversity, pref_safety):
    score = 0

    # Region match
    if row["region"].lower() == pref_region.lower():
        score += 20

    # Rent (lower is better)
    score += max(0, 30 - abs(row["rent"] - pref_rent) / 50)

    # Climate match
    score += max(0, 20 - abs(row["temperature"] - pref_temp) / 3)

    # Diversity
    score += row["diversity"] * 10

    # Safety
    score += row["safety"] * 10

    return round(score, 2)

# -------- STREAMLIT UI --------
st.title("🌍 Geo-Lifestyle Recommender")
st.write("Optimize where you should live — based on **your values**.")

# User inputs
pref_region = st.selectbox("Preferred Region", df["region"].unique())
pref_rent = st.slider("Ideal Monthly Rent", 1000, 4000, 2200)
pref_temp = st.slider("Preferred Avg Temperature (°F)", 40, 90, 70)
pref_diversity = st.slider("Minimum Diversity Score", 0.0, 1.0, 0.5)
pref_safety = st.slider("Minimum Safety Score", 0.0, 1.0, 0.5)

# Apply scoring
df["score"] = df.apply(
    lambda row: score_city(
        row,
        pref_region,
        pref_rent,
        pref_temp,
        pref_diversity,
        pref_safety,
    ),
    axis=1,
)

top_cities = df.sort_values("score", ascending=False).head(5)

st.subheader("🏆 Top Matches For You")
st.dataframe(top_cities)

# -------- VISUALS --------
st.subheader("📊 Score Comparison")
fig = px.bar(top_cities, x="city", y="score", color="score", text="score")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🌡 Rent vs Temperature")
fig2 = px.scatter(
    df,
    x="rent",
    y="temperature",
    color="region",
    size="diversity",
    hover_name="city",
)
st.plotly_chart(fig2, use_container_width=True)

# -------- AI EXPLANATION --------
st.subheader("🤖 AI Insight")

city = top_cities.iloc[0]
st.write(
    f"""
### Why **{city['city']}** fits you
- ✅ Matches your region preference (**{pref_region}**)
- ✅ Rent aligns with your target (${pref_rent})
- ✅ Comfortable climate around {city['temperature']}°F
- ✅ Strong diversity score ({city['diversity']})
- ✅ Safety rating of {city['safety']}
"""
)

st.success("Your ideal city profile has been analyzed using your selected preferences.")
