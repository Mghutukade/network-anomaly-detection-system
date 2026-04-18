from datetime import datetime

def evaluate_soc(src, dst, score):
    if score >= 85:
        severity = "CRITICAL"
    elif score >= 70:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "severity": severity,
        "time": datetime.now().strftime("%H:%M:%S")
    }