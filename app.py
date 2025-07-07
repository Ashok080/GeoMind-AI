
import pandas as pd
import streamlit as st

st.set_page_config(page_title="GeoMind AI", layout="wide")

# CSV URL
url = "https://raw.githubusercontent.com/Ashok080/GeoMind-AI/main/climate_risk.csv"

st.title("🌍 GeoMind AI – Food, Health, Climate Risk Dashboard")

try:
    df = pd.read_csv(url)
    st.success("✅ CSV loaded successfully!")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ Failed to load CSV: {e}")
