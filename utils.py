# utils.py
def calculate_hybrid_risk(predicted_cases, yolo_detections_count):
    # 1. Baseline & Threshold Calibration
    baseline_threshold = 30 
    
    # 2. Dynamic Threshold: Agar 5 se zyada garbage/water points hain toh threshold 10% kam
    if yolo_detections_count > 5:
        active_threshold = baseline_threshold * 0.9  # Yaani 27 cases
    else:
        active_threshold = baseline_threshold

    # 3. Decision Engine Categories (0-100 scale normalization)
    # Historical Risk (Normalized to 100)
    historical_risk_score = min((predicted_cases / 100) * 100, 100)
    
    # Visual Risk (Based on detections)
    visual_risk_score = min((yolo_detections_count / 10) * 100, 100)

    # 4. Weighted Risk Formula
    final_score = (0.4 * historical_risk_score) + (0.6 * visual_risk_score)

    # 5. Determine Alert Level
    if final_score > 70 or predicted_cases > 50:
        status = "🔴 HIGH RISK (Emergency Spraying)"
        advice = "Deploy 2 Spray Vans immediately and alert local hospitals."
        color = "red"
    elif final_score >= 30:
        status = "🟡 MEDIUM RISK (Cleanup Drive)"
        advice = "Organize community cleanup and remove stagnant water."
        color = "orange"
    else:
        status = "🟢 LOW RISK (Routine Monitoring)"
        advice = "Continue standard surveillance."
        color = "green"

    return final_score, status, advice, color, active_threshold