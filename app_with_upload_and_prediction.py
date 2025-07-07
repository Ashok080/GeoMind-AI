
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from sklearn.ensemble import RandomForestClassifier
from streamlit_folium import folium_static

st.set_page_config(page_title="GeoMind AI", layout="wide")

st.title("🌾 GeoMind AI – Food, Health & Climate Risk Dashboard")
st.markdown("This dashboard provides data-driven visualizations and AI-based predictions for climate, food, and health risks across regions.")

# File uploader
uploaded_file = st.file_uploader("📥 Upload your own CSV (or use default)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Custom file loaded successfully!")
else:
    url = "https://raw.githubusercontent.com/Ashok080/GeoMind-AI/main/Climate-risk-map.csv"
    df = pd.read_csv(url)
    st.info("ℹ️ Using default data from GitHub")

# Dataset Preview
with st.expander("📊 Dataset Preview & Statistics"):
    st.dataframe(df)
    st.write("Descriptive Statistics:")
    st.write(df.describe())

# Bar Chart – Food Risk
if "Food_Risk" in df.columns and "Region" in df.columns:
    st.subheader("🍚 Food Risk by Region")
    fig1 = px.bar(df, x="Region", y="Food_Risk", color="Food_Risk")
    st.plotly_chart(fig1, use_container_width=True)

# Pie Chart – Health Risk
if "Health_Risk" in df.columns:
    st.subheader("🧬 Health Risk Distribution")
    fig2 = px.pie(df, names="Health_Risk")
    st.plotly_chart(fig2, use_container_width=True)

# Line Chart – Climate Score
if "Climate_Score" in df.columns:
    st.subheader("🌡️ Climate Score per Region")
    fig3 = px.line(df, x="Region", y="Climate_Score", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

# Map with markers if lat/lon exists
if "Latitude" in df.columns and "Longitude" in df.columns:
    st.subheader("🗺️ Regional Risk Map")
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)
    for _, row in df.iterrows():
        tooltip = f"{row['Region']}<br>Food: {row['Food_Risk']}<br>Health: {row['Health_Risk']}"
        folium.Marker([row["Latitude"], row["Longitude"]], tooltip=tooltip).add_to(m)
    folium_static(m)

# ML Prediction Section
st.subheader("🤖 AI Risk Predictor (Random Forest)")

# Encode categorical labels
df_model = df.copy()
if "Food_Risk" in df.columns and "Health_Risk" in df.columns:
    df_model["Food_Risk_Encoded"] = df_model["Food_Risk"].astype("category").cat.codes
    df_model["Health_Risk_Encoded"] = df_model["Health_Risk"].astype("category").cat.codes

    features = ["Temperature", "Rainfall", "Climate_Score"]
    if all(f in df.columns for f in features):
        X = df_model[features]
        y_food = df_model["Food_Risk_Encoded"]
        y_health = df_model["Health_Risk_Encoded"]

        rf_food = RandomForestClassifier().fit(X, y_food)
        rf_health = RandomForestClassifier().fit(X, y_health)

        # Input sliders
        st.markdown("### 🌦️ Enter Climate Inputs for Prediction:")
        temp = st.slider("Temperature (°C)", min_value=20.0, max_value=45.0, value=30.0)
        rain = st.slider("Rainfall (mm)", min_value=50, max_value=300, value=150)
        score = st.slider("Climate Score", min_value=0.0, max_value=1.0, value=0.5)

        input_df = pd.DataFrame([[temp, rain, score]], columns=features)

        pred_food = rf_food.predict(input_df)[0]
        pred_health = rf_health.predict(input_df)[0]

        food_labels = df_model["Food_Risk"].astype("category").cat.categories
        health_labels = df_model["Health_Risk"].astype("category").cat.categories

        st.success(f"🧠 Predicted Food Risk: **{food_labels[pred_food]}**")
        st.success(f"🧠 Predicted Health Risk: **{health_labels[pred_health]}**")
    else:
        st.warning("⚠️ Required features missing for prediction.")
else:
    st.warning("⚠️ 'Food_Risk' or 'Health_Risk' columns missing.")

st.markdown("---")
st.caption("Built by Ashok Miji • GeoMind AI Project • Powered by Streamlit")
