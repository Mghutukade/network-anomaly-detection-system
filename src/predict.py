import joblib
import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_if = joblib.load(os.path.join(BASE, "model_if.pkl"))
model_rf = joblib.load(os.path.join(BASE, "model_rf.pkl"))
scaler = joblib.load(os.path.join(BASE, "scaler.pkl"))

FEATURES = ["packets","bytes","duration","proto","syn","ack","entropy"]

def hybrid_score(features):

    df = pd.DataFrame([features], columns=FEATURES)
    scaled = scaler.transform(df)

    # -----------------------------
    # Isolation Forest
    # -----------------------------
    if_score = model_if.decision_function(scaled)[0]
    if_score = int((1 - if_score) * 50)
    if_score = max(0, min(100, if_score))

    # -----------------------------
    # Random Forest
    # -----------------------------
    rf_score = model_rf.predict_proba(scaled)[0][1]
    rf_score = int(rf_score * 100)

    # -----------------------------
    # HYBRID FUSION
    # -----------------------------
    final_score = int(
        (0.6 * if_score) +   # anomaly weight
        (0.4 * rf_score)
    )

    # DEBUG (optional)
    # print(f"IF={if_score}, RF={rf_score}, FINAL={final_score}")

    return final_score


def get_label(score):
    if score > 80:
        return "CRITICAL"
    elif score > 60:
        return "HIGH"
    elif score > 40:
        return "MEDIUM"
    else:
        return "LOW"