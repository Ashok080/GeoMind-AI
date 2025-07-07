
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="GeoMind AI", layout="wide")

st.title("🌾 GeoMind AI – Food, Health & Climate Risk Dashboard")
st.markdown("This dashboard visualizes regional risks based on climate, food, and health factors.")

# Load dataset from GitHub raw URL
url = "https://raw.githubusercontent.com/Ashok080/GeoMind-AI/main/Climate-risk.csv"
try:
    df = pd.read_csv(url)
    st.success("✅ Climate-risk.csv loaded successfully!")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Basic stats
with st.expander("📊 Dataset Preview & Statistics"):
    st.dataframe(df)
    st.write("Descriptive Statistics:")
    st.write(df.describe())

# Plotly bar chart for Food Risk by Region
st.subheader("🍚 Food Risk by Region")
fig_food = px.bar(df, x="Region", y="Food_Risk", color="Food_Risk", title="Food Risk Level by Region")
st.plotly_chart(fig_food, use_container_width=True)

# Plotly pie chart for Health Risk Distribution
st.subheader("🧬 Health Risk Distribution")
fig_health = px.pie(df, names="Health_Risk", title="Health Risk Proportion")
st.plotly_chart(fig_health, use_container_width=True)

# Plotly Climate Score Chart
st.subheader("🌡️ Climate Score per Region")
fig_climate = px.line(df, x="Region", y="Climate_Score", markers=True, title="Climate Risk Score")
st.plotly_chart(fig_climate, use_container_width=True)

# Add a simple map if coordinates are available
if "Latitude" in df.columns and "Longitude" in df.columns:
    st.subheader("🗺️ Risk Map (requires lat/lon)")
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)
    for _, row in df.iterrows():
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            tooltip=f"{row['Region']}<br>Food: {row['Food_Risk']}<br>Health: {row['Health_Risk']}",
            icon=folium.Icon(color="red")
        ).add_to(m)
    folium_static(m)
else:
    st.info("ℹ️ Map not shown — 'Latitude' and 'Longitude' columns missing in CSV.")

st.markdown("---")
st.caption("Built by Ashok Miji • GeoMind AI Project • Streamlit + GitHub")
