import streamlit as st
import pandas as pd
import joblib
from ultralytics import YOLO
from PIL import Image
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from utils import calculate_hybrid_risk

# --- 1. Page Config & Professional Styling ---
st.set_page_config(page_title="Eco-Sentinel Pro | Intelligence Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    .stAlert { border-radius: 12px; }
    h1, h2, h3 { color: #f3f4f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Model Loading ---
@st.cache_resource
def load_resources():
    # Paths adjusted to your folder structure
    vision_model = YOLO('models/yolo_vision/best.pt') 
    trend_model = joblib.load('models/trend_analysis/dengue_xgboost_model.pkt')
    return vision_model, trend_model

vision_engine, trend_engine = load_resources()

# --- 3. Sidebar (No San Juan - Only Pakistan Cities) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2760/2760147.png", width=80)
    st.title("Control Panel")
    selected_city = st.selectbox("🎯 Target Region", ["Karachi", "Lahore"])
    selected_month = st.select_slider("📅 Forecast Month", options=list(range(1, 13)))
    conf_threshold = st.sidebar.slider("🔍 Detection Sensitivity", 0.1, 1.0, 0.4)
    st.divider()
    st.caption("System Status: Operational 🟢")

# --- 4. Main Dashboard UI ---
st.title("🛡️ Eco-Sentinel Pro: Hybrid Outbreak Intelligence")

uploaded_file = st.file_uploader("📤 Upload Field Surveillance Data (Video or Image)", type=["mp4", "jpg", "jpeg", "png"])

# Initial State: Agar file upload nahi hui toh Dashboard clean rakho
if not uploaded_file:
    st.info("👋 Welcome. Please upload area surveillance data to generate the Outbreak Risk Intelligence report.")
    # Default Map of Pakistan
    m_default = folium.Map(location=[30.3753, 69.3451], zoom_start=5, tiles="cartodbpositron")
    st_folium(m_default, width=1200, height=450)
else:
    # Processing Layout
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("📡 Field Hazard Analysis") # Replaced YOLO Label
        img = Image.open(uploaded_file)
        results = vision_engine.predict(img, conf=conf_threshold)
        detections_count = len(results[0].boxes)
        st.image(results[0].plot(), caption="Identified Potential Breeding Hazards", use_column_width=True)

    with col2:
        st.subheader("📊 Intelligence Summary") # Replaced XGBoost Label
        
        # Data Encoding for Karachi/Lahore
        city_enc = 0 if selected_city == "Karachi" else 1
        # Prediction Input (Using month for seasonality)
        pred_input = pd.DataFrame([[city_enc, selected_month*4, 75, 298, 75]], 
                                  columns=['city_encoded', 'weekofyear', 'reanalysis_relative_humidity_percent', 'reanalysis_avg_temp_k', 'reanalysis_relative_humidity_percent_lag4'])
        predicted_cases = trend_engine.predict(pred_input)[0]
        
        # Decision Engine Logic (utils.py se linked)
        score, status, advice, color, threshold = calculate_hybrid_risk(predicted_cases, detections_count)

        # Visualizing Metrics
        st.metric("Predicted Outbreak Intensity", f"{int(predicted_cases)} Cases")
        st.write(f"**Composite Risk Score: {int(score)}/100**")
        st.progress(int(score)/100)
        
        st.markdown(f"### Current Status: :{color}[{status}]")
        
        st.divider()
        st.subheader("📢 Decision Intelligence")
        st.success(f"**Actionable Advice:** \n\n {advice}")

    # --- 5. High-Res Heatmap Section ---
    st.divider()
    st.subheader(f"📍 Risk Density Heatmap: {selected_city} Districts")
    
    try:
        coords_df = pd.read_csv('data/processed/city_coords.csv')
        city_data = coords_df[coords_df['City'] == selected_city]
        
        # Professional Map Setup
        m = folium.Map(location=[city_data['Lat'].mean(), city_data['Lon'].mean()], zoom_start=12, tiles="cartodbpositron")
        
        # Heatmap Layer (Color Glow)
        heat_data = [[row['Lat'], row['Lon'], score/100] for index, row in city_data.iterrows()]
        HeatMap(heat_data, radius=25, blur=15, min_opacity=0.5).add_to(m)
        
        # Markers for Districts
        for _, row in city_data.iterrows():
            folium.CircleMarker(
                location=[row['Lat'], row['Lon']],
                radius=6,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=f"District: {row['Area_Name']}<br>Status: {status}"
            ).add_to(m)
            
        st_folium(m, width=1200, height=500)
    except Exception as e:
        st.error(f"Mapping System Offline: {e}")