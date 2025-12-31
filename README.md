🛡️ Eco-Sentinel Pro: AI-Driven Dengue Risk Detector
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