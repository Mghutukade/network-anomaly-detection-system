import joblib
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

FEATURES = [
    "packets",
    "bytes",
    "duration",
    "proto",
    "syn",
    "ack",
    "entropy"
]

# -----------------------------
# ML PREDICTION
# -----------------------------
def predict_traffic(features):
    df = pd.DataFrame([features], columns=FEATURES)
    df_scaled = scaler.transform(df)

    prob = model.predict_proba(df_scaled)[0][1]
    return prob


# -----------------------------
# RISK LABEL FUNCTION (FIXED)
# -----------------------------
def get_risk_label(score):
    score = int(score * 100)

    if score > 80:
        return f"🚨 HIGH RISK ({score}%)"
    elif score > 50:
        return f"⚠️ MEDIUM RISK ({score}%)"
    else:
        return f"✅ LOW RISK ({score}%)"