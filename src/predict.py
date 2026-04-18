import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model.pkl")

if not os.path.exists(model_path):
    raise FileNotFoundError("❌ model.pkl not found! Run training first.")

model = joblib.load(model_path)

# IMPORTANT: same feature names used in training
FEATURE_NAMES = ["packet_length", "protocol", "src_port", "dst_port", "flags"]


def predict_traffic(data):
    df = pd.DataFrame([data], columns=FEATURE_NAMES)
    prediction = model.predict(df)
    return prediction[0]


def get_risk_label(pred):
    return "🚨 Attack Detected" if pred == 1 else "✅ Normal"