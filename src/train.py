import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# -----------------------------
# DATA (Better balanced)
# -----------------------------
data = {
    "packets": [5, 10, 50, 200, 300, 20, 100, 400],
    "bytes": [500, 800, 5000, 20000, 30000, 2000, 10000, 40000],
    "duration": [1, 2, 2, 5, 10, 2, 3, 8],
    "proto": [6, 6, 6, 17, 17, 6, 6, 17],
    "syn": [1, 2, 10, 50, 90, 2, 5, 120],
    "ack": [1, 2, 5, 10, 2, 1, 3, 1],
    "entropy": [1.2, 1.5, 3, 6, 7, 2, 3, 8],
    "label": [0, 0, 0, 1, 1, 0, 0, 1]
}

df = pd.DataFrame(data)

X = df.drop("label", axis=1)
y = df["label"]

# -----------------------------
# SCALER
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# MODELS
# -----------------------------
model_if = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model_if.fit(X_scaled)

model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X_scaled, y)

# -----------------------------
# SAVE
# -----------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

joblib.dump(model_if, os.path.join(BASE, "model_if.pkl"))
joblib.dump(model_rf, os.path.join(BASE, "model_rf.pkl"))
joblib.dump(scaler, os.path.join(BASE, "scaler.pkl"))

print("✅ Hybrid models trained successfully")