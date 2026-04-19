from flask import Flask
from flask_socketio import SocketIO
import joblib
import os 
import numpy as np
import threading
import time

# =========================
# Flask + SocketIO Setup
# =========================
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

# =========================
# Load ML Models
# =========================
# This gets the directory where app.py is located (D:\Network_Anomaly_Detection\src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Now it looks in that same folder for the .pkl files
rf_model = joblib.load(os.path.join(BASE_DIR, "rf_model.pkl"))
iso_model = joblib.load(os.path.join(BASE_DIR, "iso_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# =========================
# Prediction Function
# =========================
def predict(features):
    """
    Hybrid detection logic:
    RF + Isolation Forest
    """
    features = np.array(features).reshape(1, -1)
    scaled = scaler.transform(features)

    rf_pred = rf_model.predict(scaled)[0]

    # Isolation Forest: -1 = anomaly, 1 = normal
    iso_pred = iso_model.predict(scaled)[0]

    if rf_pred == 1 or iso_pred == -1:
        return "ANOMALY"
    return "NORMAL"


# =========================
# REAL PACKET PROCESSOR
# =========================
def process_packet(features):
    result = predict(features)
    print(f"Result: {result}")
    socketio.emit("packet", {
        "status": result
    })


# =========================
# SIMULATED STREAM (replace with sniffer)
# =========================
def fake_sniffer_stream():
    """
    REMOVE THIS once you connect real sniffer.py
    """
    while True:
        # Fake feature vector (replace with real packet features)
        features = np.random.rand(scaler.n_features_in_)

        process_packet(features)
        time.sleep(1)


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return "NADS Backend Running (SOC Engine Active)"


# =========================
# SOCKET EVENTS
# =========================
@socketio.on("connect")
def handle_connect():
    print("Frontend Connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Frontend Disconnected")


# Optional control event (start/stop future upgrade)
@socketio.on("toggle")
def handle_toggle():
    print("Toggle received from dashboard")


# =========================
# MAIN
# =========================
if __name__ == '__main__':
    # --- ADD THIS START ---
    print("🚀 Starting background simulation thread...")
    thread = threading.Thread(target=fake_sniffer_stream)
    thread.daemon = True # This ensures the thread closes when you stop the app
    thread.start()
    # --- ADD THIS END ---

    print("🚀 Starting NADS SOC Backend...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)