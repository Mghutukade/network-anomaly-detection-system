import joblib
import os
import pandas as pd

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")

# Load model
if not os.path.exists(model_path):
    raise FileNotFoundError("❌ model.pkl not found! Run training first.")

model = joblib.load(model_path)

# Feature names (IMPORTANT)
FEATURE_NAMES = ["packet_length", "protocol", "src_port", "dst_port", "flags"]


def predict_traffic(data):
    # data format:
    # [packet_length, protocol, src_port, dst_port, flags]

    packet_length, protocol, src_port, dst_port, flags = data

    # 🔥 ADD YOUR RULE HERE
    if protocol == 17:
        return 0

    if packet_length > 1200:
        return 1

    # ML Prediction
    df = pd.DataFrame([data], columns=FEATURE_NAMES)
    prediction = model.predict(df)

    return prediction[0]

    # ML Prediction
    prediction = model.predict(df)
    return prediction[0]


def get_risk_label(pred):
    return "🚨 Attack Detected" if pred == 1 else "✅ Normal"