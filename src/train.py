import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Create dummy dataset with SAME features as live capture
data = {
    "packet_length": [60, 500, 1000, 70, 1500],
    "protocol": [6, 6, 17, 6, 17],
    "src_port": [1234, 443, 80, 22, 8080],
    "dst_port": [80, 1234, 53, 443, 21],
    "flags": [1, 1, 0, 1, 0],
    "label": [0, 0, 1, 0, 1]  # 0=Normal, 1=Attack
}

df = pd.DataFrame(data)

X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier()
model.fit(X, y)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")

joblib.dump(model, model_path)

print("✅ Model trained successfully!")
print("✅ Model saved at:", model_path)