def calculate_hybrid_risk(predicted_cases, yolo_detections_count):
    # 1. Negative Fix: Agar model -1.2 de toh usay 0 kar do
    predicted_cases = max(0, predicted_cases)
    yolo_detections_count = max(0, yolo_detections_count)

    # 2. Baseline & Threshold Calibration
    baseline_threshold = 30 
    
    # 3. Dynamic Threshold
    if yolo_detections_count > 5:
        active_threshold = baseline_threshold * 0.9  # 27 cases
    else:
        active_threshold = baseline_threshold

    # 4. Normalization (Khubsurat Scaling 0-100)
    historical_risk_score = min((predicted_cases / 100) * 100, 100)
    visual_risk_score = min((yolo_detections_count / 10) * 100, 100)

    # 5. Weighted Risk Formula (Historical 40% + Visual 60%)
    final_score = (0.4 * historical_risk_score) + (0.6 * visual_risk_score)
    final_score = round(final_score, 1) # Decimal point fix

    # 6. Determine Alert Level & Resources
    if final_score > 70 or predicted_cases > 50:
        status = "CRITICAL VECTOR OUTBREAK"
        advice = "Deploy 2-3 Fumigation Units immediately and alert local hospitals."
        color = "red"
        vans = "3 Fumigation Units"
        workers = "20 Personnel (Emergency Response)"
    elif final_score >= 30:
        status = "ELEVATED VECTOR ALERT"
        advice = "Organize community cleanup and remove stagnant water."
        color = "orange"
        vans = "1 Fumigation Unit"
        workers = "10 Personnel (Targeted Control)"
    else:
        status = "LOW RISK (Routine Monitoring)"
        advice = "Continue standard surveillance. No immediate emergency action."
        color = "green"
        vans = "0 Units (Monitoring Only)"
        workers = "2 Personnel (Surveyors Only)"

    return final_score, status, advice, color, active_threshold, vans, workers