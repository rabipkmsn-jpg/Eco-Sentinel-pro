🛡️ Eco-Sentinel Pro: AI-Driven Vector-Borne Disease Intelligence
🌟 1. Project Introduction
Eco-Sentinel Pro is an innovative public health monitoring system that integrates Artificial Intelligence (AI) and Data Analytics to identify Dengue risks before they escalate into outbreaks. The system specifically targets high-risk environmental factors such as Standing Water and Garbage accumulation, which serve as primary breeding grounds for Aedes aegypti mosquitoes.

🎯 2. Objectives
Automated Detection: Utilize the YOLOv8 (You Only Look Once) architecture to identify and localize environmental hazards in real-time images.

Risk Mapping: Integrate geographical coordinates to visualize "High-Risk" zones using interactive heatmaps.

Data-Driven Prevention: Combine visual analysis with historical outbreak data to provide a proactive alert system for municipal authorities.

🚧 3. Hurdles & Blockers (Challenges Overcome)
Developing this project involved overcoming several technical and logistical challenges:

Data Scarcity & Quality: Initially, finding high-quality, localized images of garbage and standing water was challenging. A specialized dataset was curated and augmented to ensure model robustness.

Annotation Intensity: Manually labeling 166+ images for "Garbage" and "Standing Water" classes required high precision to avoid false positives during training.

Dataset Configuration (YAML Errors): During the training phase, significant pathing issues occurred within the YOLO environment. This was resolved by manually restructuring the data.yaml file and re-pointing training/validation directories.

Model Optimization: Achieving an accuracy of 95.9% (mAP50) with a relatively small dataset (166 images) was a major hurdle. This was achieved through fine-tuning the YOLOv8 Nano model over 100 epochs.

Integration Complexity: Transitioning the model from a cloud-based environment (Google Colab) to a local production environment (VS Code) required resolving library dependencies (OpenCV, Streamlit) and managing file serialization.

📂 4. Project Structure
Plaintext

Eco-Sentinel-Pro/
├── assets/             # Test images and demo videos for validation
├── data/
│   ├── raw/            # Historical Dengue dataset (CSV format)
│   ├── processed/      # Curated geographical data (city_coords.csv)
├── metadata/           # Configuration files and data.yaml
├── models/             # Serialized YOLOv8 weights (best.pt)
├── app.py              # Main application logic (Streamlit Dashboard)
├── requirements.txt    # Python dependency manifest
└── README.md           # Project documentation and guide
🛠️ 5. Technology Stack
Computer Vision: YOLOv8 (Ultralytics)

Web Framework: Streamlit

Programming Language: Python 3.12

Data Visualization: Folium (Heatmaps), Pandas, and Matplotlib
🚀 6. Phase 2: Professional Refinement (Today's Updates)
In the latest development cycle, the system was upgraded from a basic detection tool to a Decision Support System (DSS) with professional-grade UI/UX and logical accuracy.

🆕 Advanced Features Added:
Vector-Borne Disease Branding: Transitioned from generic labels to professional terminology ("Vector-Borne Disease Intelligence"), making it suitable for institutional and governmental use.

Dynamic Resource Allocation: Integrated a smart logic engine that calculates the exact number of Fumigation Units and Field Personnel required based on the real-time risk score.

Session-State Hard Reset: Developed a custom "Hard Reset" mechanism that clears the cache and file uploader, allowing for seamless back-to-back regional analysis.

Hybrid Risk Indexing: Refined the calculation formula to weight visual hazards (YOLOv8) and historical trends (XGBoost) at a 60/40 ratio, ensuring a balanced risk assessment.

⚡ Technical Hurdles Resolved (Today's Blockers):
Negative Value Handling: Fixed a critical bug where the XGBoost model would predict negative values for low-incidence months. This was resolved using max(0, predicted_cases) normalization.

Dynamic Grid Layout: Overcame Streamlit's linear layout constraints by implementing a Multi-Column Grid System, placing the Interactive Heatmap at the top-right for optimal dashboard scannability.

Library Dependency Issues: Resolved ModuleNotFoundError: plotly by synchronizing the local environment with the advanced visualization engine.

Real-time Logic Calibration: Addressed the "Static Resource" issue where low-risk areas were still being assigned high personnel. Optimized the code to reflect 0 Units for routine monitoring, ensuring logical field operations.

📊 7. Model Performance Metrics

Detection Accuracy: 95.9% mAP50 (YOLOv8)
Predictive Trend Accuracy: Optimized XGBoost model for regional forecasting.
Risk Scaling: 0-100 Normalized Hybrid Score.

How to Run the Updated System

Install dependencies: pip install -r requirements.txt
Launch the Dashboard: py -m streamlit run app.py
Process: Select Region → Upload Image → Receive Real-time Actionable Protocol.

🔮 8. Futuristic Vision & Scaling (Closing Statement)

Eco-Sentinel Pro is not just a dashboard; it is a blueprint for the future of Smart Public Health Surveillance. Our roadmap for future integration includes:

Real-time Drone Integration: Transitioning from static image uploads to live drone feeds for automated aerial surveillance of inaccessible urban slums.

IoT Sensor Fusion: Integrating local weather station data and IoT-enabled stagnant water sensors for real-time 24/7 monitoring.

Automated Response Dispatch: Linking the resource allocation engine directly with municipal department APIs to auto-assign fumigation teams as soon as a 'Critical' risk is detected.






<img width="1833" height="790" alt="Screenshot 2025-12-31 145805" src="https://github.com/user-attachments/assets/60e0f715-3811-488d-9fb1-506923d3b5ed" />


<img width="1795" height="872" alt="Screenshot 2025-12-31 144223" src="https://github.com/user-attachments/assets/e892d6fb-d596-46a0-963b-7875efee31c3" />


<img width="1759" height="789" alt="Screenshot 2025-12-31 145859" src="https://github.com/user-attachments/assets/55ccd17e-75b2-4870-be51-d8373005fab0" />

