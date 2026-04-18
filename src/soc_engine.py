# src/soc_engine.py
from collections import defaultdict
import time

incidents = defaultdict(list)

def evaluate_soc(src, dst, score):

    key = f"{src}->{dst}"
    timestamp = time.strftime("%H:%M:%S")

    # store history
    incidents[key].append(score)

    avg_score = sum(incidents[key][-5:]) / len(incidents[key][-5:])

    severity = "LOW"

    if avg_score > 80:
        severity = "CRITICAL"
    elif avg_score > 60:
        severity = "HIGH"
    elif avg_score > 40:
        severity = "MEDIUM"

    return {
        "flow": key,
        "avg_score": round(avg_score, 2),
        "severity": severity,
        "time": timestamp
    }