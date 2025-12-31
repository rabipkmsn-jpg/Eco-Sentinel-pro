import streamlit as st
import pandas as pd
import joblib
from ultralytics import YOLO
from PIL import Image
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.graph_objects as go
from utils import calculate_hybrid_risk

# --- 1. Page Configuration ---
st.set_page_config(page_title="Eco-Sentinel Pro | Vector-Borne Disease Intelligence", layout="wide")

# Session State for Hard Reset
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = 0

# Custom CSS for Professional Branding
st.markdown("""
    <style>
    .metric-card { background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; }
    .status-card { background-color: #111827; padding: 20px; border-radius: 15px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_models():
    return YOLO('models/yolo_vision/best.pt'), joblib.load('models/trend_analysis/dengue_xgboost_model.pkt')

vision_engine, trend_engine = load_models()

# --- 2. Sidebar (Vector Control Panel) ---
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
with st.sidebar:
    st.title("🦟 Vector Control Panel") 
    selected_city = st.selectbox("🎯 Target Region", ["Karachi", "Lahore"])
    selected_month = st.selectbox("📅 Forecast Month", months)
    month_idx = months.index(selected_month) + 1
    conf_threshold = st.slider("🔍 Detection Sensitivity", 0.1, 1.0, 0.4)
    
    st.divider()
    if st.button("🔄 Reset & Clear All", use_container_width=True):
        st.session_state['uploader_key'] += 1 
        st.rerun()
        
    st.divider()
    st.success("Vector Surveillance: Operational 🟢")

# --- 3. Main Layout Structure ---
st.title("🛡️ Eco-Sentinel Pro: Vector-Borne Disease Intelligence") 
st.markdown("#### *Advanced AI-Powered Hybrid Outbreak Prediction & Decision Engine*")

# Top Section: File Uploader & Map
top_col1, top_col2 = st.columns([1, 2])

with top_col1:
    st.subheader("📤 Breeding Site Assessment") 
    uploaded_file = st.file_uploader("Upload Surveillance Data (Stagnant Water/Hazards)", 
                                     type=["jpg", "png", "jpeg"], 
                                     key=f"uploader_{st.session_state['uploader_key']}")
    
with top_col2:
    st.subheader(f"📍 Vector-Borne Risk Heatmap: {selected_city}") 
    try:
        coords_df = pd.read_csv('data/processed/city_coords.csv')
        city_data = coords_df[coords_df['City'].str.contains(selected_city, case=False)]
        m = folium.Map(location=[city_data['Lat'].mean(), city_data['Lon'].mean()], zoom_start=11, tiles="cartodbpositron")
        
        if uploaded_file:
            heat_data = [[row['Lat'], row['Lon'], 0.8] for _, row in city_data.iterrows()]
            HeatMap(heat_data, radius=25, blur=15).add_to(m)
        
        st_folium(m, width=900, height=350, key="main_map")
    except:
        st.warning("Mapping Engine Loading...")

st.divider()

# Analysis Section
if uploaded_file:
    mid_col1, mid_col2 = st.columns([1.5, 1])
    
    with mid_col1:
        st.subheader("📡 Field Hazard Identification") 
        img = Image.open(uploaded_file)
        results = vision_engine.predict(img, conf=conf_threshold)
        detections = len(results[0].boxes)
        st.image(results[0].plot(), use_container_width=True, caption="Visual Identification of Larval Habitats")

    with mid_col2:
        st.subheader("📊 Transmission Risk Index") 
        city_enc = 0 if selected_city == "Karachi" else 1
        pred_input = pd.DataFrame([[city_enc, month_idx*4, 75, 298, 75]], 
                                  columns=['city_encoded', 'weekofyear', 'reanalysis_relative_humidity_percent', 'reanalysis_avg_temp_k', 'reanalysis_relative_humidity_percent_lag4'])
        predicted_cases = int(trend_engine.predict(pred_input)[0])
        
        # Updated to catch ALL 7 return values from your beautiful new utils logic
        score, status, advice, color, threshold, vans_needed, workers_needed = calculate_hybrid_risk(predicted_cases, detections)

        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = score,
            title = {'text': "Hybrid Risk Score (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': color},
                     'steps': [{'range': [0, 30], 'color': "green"}, {'range': [70, 100], 'color': "red"}]}))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    bot_col1, bot_col2 = st.columns(2)
    
    with bot_col1:
        st.subheader("📋 Response Protocol")
        st.markdown(f"""<div class="status-card" style="border-top: 5px solid {color};">
            <h3 style="color:{color}">{status}</h3>
            <p><b>Recommended Action:</b> {advice}</p>
        </div>""", unsafe_allow_html=True)

    with bot_col2:
        st.subheader("🛠️ Strategic Resource Allocation")
        # Ab ye values directly utils se aa rahi hain, koi fix manual nahi hai
        st.markdown(f"""<div class="status-card">
            <p>🚚 <b>Anti-Vector Vehicles:</b> {vans_needed}</p>
            <p>👥 <b>Field Personnel:</b> {workers_needed}</p>
            <p>🧪 <b>Larvicide Inventory:</b> {"High Priority" if score > 50 else "Standard Stock"} for {selected_city}</p>
        </div>""", unsafe_allow_html=True)
else:
    st.info("💡 Strategic Advice: Upload larval habitat data to initiate the Vector-Borne Disease Intelligence engine.")