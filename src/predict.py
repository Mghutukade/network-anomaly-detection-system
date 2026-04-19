import numpy as np
import joblib
import os

# This gets D:\Network_Anomaly_Detection\src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the models WITHOUT adding an extra "src" to the path
rf_model = joblib.load(os.path.join(BASE_DIR, "rf_model.pkl"))
iso_model = joblib.load(os.path.join(BASE_DIR, "iso_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

def hybrid_score(features):
    """
    features = pandas DataFrame with 1 row
    """

    # ✅ DO NOT WRAP AGAIN
    scaled = scaler.transform(features)

    # RF probability
    rf_prob = rf_model.predict_proba(scaled)[0][1]

    # Isolation Forest score
    iso_score = iso_model.decision_function(scaled)[0]

    # Normalize iso (-0.5 to 0.5 approx → 0 to 1)
    iso_norm = (iso_score + 0.5)

    # Combine
    final_score = (0.7 * rf_prob + 0.3 * iso_norm) * 100

    return int(final_score)