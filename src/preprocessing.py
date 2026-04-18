import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_data(path):
    df = pd.read_csv(path, low_memory=False)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Feature creation
    df["packets"] = df["Total Fwd Packets"] + df["Total Backward Packets"]
    df["bytes"] = df["Total Length of Fwd Packets"] + df["Total Length of Bwd Packets"]
    df["duration"] = df["Flow Duration"]
    df["protocol"] = 6
    df["length"] = df["Packet Length Mean"]
    df["syn"] = df["SYN Flag Count"]
    df["ack"] = df["ACK Flag Count"]
    df["entropy"] = 0

    # ✅ FIX LABEL
    df["label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

    # Clean data
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Convert ALL to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)

    # Derived features
    df["avg_packet_size"] = df["bytes"] / df["packets"].replace(0, 1)
    df["packet_rate"] = df["packets"] / df["duration"].replace(0, 1)
    df["byte_rate"] = df["bytes"] / df["duration"].replace(0, 1)

    # Final features
    features = [
        "packets", "bytes", "duration", "protocol", "length",
        "avg_packet_size", "packet_rate", "byte_rate",
        "syn", "ack", "entropy"
    ]

    X = df[features]
    y = df["label"]

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler