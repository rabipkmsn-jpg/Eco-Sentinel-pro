import streamlit as st
import pandas as pd
import joblib
from ultralytics import YOLO
from PIL import Image
import folium
from streamlit_folium import st_folium
from utils import calculate_hybrid_risk

# --- Configuration & Styling ---
st.set_page_config(page_title="Eco-Sentinel Pro V2", layout="wide")
st.markdown("""<style>.main { background-color: #f5f7f9; } .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }</style>""", unsafe_allow_html=True)

# --- Load Models ---
@st.cache_resource
def load_models():
    yolo = YOLO('models/yolo_vision/best.pt')  # Path updated to your folder
    xgb = joblib.load('models/trend_analysis/dengue_xgboost_model.pkt')
    return yolo, xgb

vision_model, trend_model = load_models()

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2760/2760147.png", width=100)
st.sidebar.title("Control Panel")
selected_city = st.sidebar.selectbox("Select Target City", ["San Juan (sj)", "Iquitos (iq)"])
selected_month = st.sidebar.select_slider("Select Month", options=list(range(1, 13)))
conf_threshold = st.sidebar.slider("Detection Confidence", 0.1, 1.0, 0.4)

# --- Phase 4: Input Panel ---
st.title("🛡️ Eco-Sentinel Pro: Hybrid Outbreak Intelligence")
uploaded_video = st.file_uploader("Upload Area Video/Image (10-sec limit for analysis)", type=["mp4", "jpg", "jpeg", "png"])

col1, col2 = st.columns([1.5, 1])

# --- Processing Logic ---
with col1:
    st.subheader("🔍 Visual Analytics (YOLOv8)")
    detections_count = 0
    if uploaded_video:
        # Display image/frame
        img = Image.open(uploaded_video)
        results = vision_model.predict(img, conf=conf_threshold)
        detections_count = len(results[0].boxes)
        st.image(results[0].plot(), caption=f"Detected Hazards: {detections_count}", use_column_width=True)
    else:
        st.info("Please upload visual data to start analysis.")

with col2:
    st.subheader("📈 Trend Forecast (XGBoost)")
    # Mock input for historical prediction (integration with your model)
    city_enc = 0 if "San Juan" in selected_city else 1
    # Note: Lags can be hardcoded or taken from a hidden data file for simplicity here
    pred_input = pd.DataFrame([[city_enc, 20, 75, 298, 75]], columns=['city_encoded', 'weekofyear', 'reanalysis_relative_humidity_percent', 'reanalysis_avg_temp_k', 'reanalysis_relative_humidity_percent_lag4'])
    predicted_cases = trend_model.predict(pred_input)[0]
    
    st.metric("Predicted Cases", f"{int(predicted_cases)}")

    # --- Phase 3: Hybrid Decision Engine ---
    score, status, advice, color, threshold = calculate_hybrid_risk(predicted_cases, detections_count)
    
    st.divider()
    st.subheader("📢 Decision Engine Output")
    st.markdown(f"### Score: <span style='color:{color}'>{int(score)}/100</span>", unsafe_allow_html=True)
    st.info(f"**Current Status:** {status}")
    
    if predicted_cases > threshold:
        st.error(f"⚠️ OUTBREAK DETECTED: Cases ({int(predicted_cases)}) exceeded Dynamic Threshold ({int(threshold)})")
    
    st.success(f"**Actionable Advice:** {advice}")

# --- Output Panel 2: Interactive Map ---
st.divider()
st.subheader("📍 Interactive Regional Risk Map")
# Load coordinates
try:
    coords = pd.read_csv('data/processed/city_coords.csv') # Make sure this file exists
    m = folium.Map(location=[coords['lat'].mean(), coords['lon'].mean()], zoom_start=5)
    
    for _, row in coords.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=20000,
            color=color,
            fill=True,
            popup=f"{selected_city}: {status}"
        ).add_to(m)
    st_folium(m, width=1200, height=400)
except:
    st.warning("Map coordinates not found. Please check city_coords.csv")