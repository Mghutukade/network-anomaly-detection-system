import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# -----------------------------
# SAMPLE DATA (FLOW BASED IDS)
# -----------------------------
data = {
    "packets": [5, 50, 200, 10, 300, 20, 100, 400],
    "bytes": [500, 5000, 20000, 1000, 30000, 2000, 10000, 40000],
    "duration": [1, 2, 5, 1, 10, 2, 3, 8],
    "proto": [6, 6, 17, 6, 17, 6, 6, 17],
    "syn": [0, 10, 50, 1, 90, 2, 5, 120],
    "ack": [1, 5, 10, 1, 2, 1, 3, 1],
    "entropy": [1, 3, 6, 1, 7, 2, 3, 8],
    "label": [0, 0, 1, 0, 1, 0, 0, 1]
}

df = pd.DataFrame(data)

X = df.drop("label", axis=1)
y = df["label"]

# -----------------------------
# SCALE
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)

# -----------------------------
# SAVE SAFE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(scaler, os.path.join(BASE_DIR, "scaler.pkl"))

print("✅ Training completed successfully")