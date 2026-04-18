from scapy.all import sniff, IP, TCP, Raw
import numpy as np
import time
import math

flows = {}

# -----------------------------
# ENTROPY FUNCTION
# -----------------------------
def calculate_entropy(data):
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    return -sum([p * math.log2(p) for p in prob])

# -----------------------------
# PROCESS PACKET
# -----------------------------
def process_packet(packet, model, scaler):
    if not packet.haslayer(IP):
        return

    src = packet[IP].src
    dst = packet[IP].dst
    proto = packet[IP].proto
    length = len(packet)
    now = time.time()

    key = (src, dst)

    # Ignore ICMP
    if proto == 1:
        return

    # -----------------------------
    # FLOW INIT
    # -----------------------------
    if key not in flows:
        flows[key] = {
            "count": 0,
            "bytes": 0,
            "start": now,
            "syn": 0,
            "ack": 0
        }

    flows[key]["count"] += 1
    flows[key]["bytes"] += length

    packets = flows[key]["count"]
    bytes_ = flows[key]["bytes"]
    duration = now - flows[key]["start"]

    # Reset flow
    if duration > 30:
        flows[key] = {
            "count": 1,
            "bytes": length,
            "start": now,
            "syn": 0,
            "ack": 0
        }
        return

    # -----------------------------
    # TCP FLAGS
    # -----------------------------
    syn_flag = 0
    ack_flag = 0

    if packet.haslayer(TCP):
        flags = packet[TCP].flags
        if flags & 0x02:
            syn_flag = 1
        if flags & 0x10:
            ack_flag = 1

    flows[key]["syn"] += syn_flag
    flows[key]["ack"] += ack_flag

    # -----------------------------
    # ENTROPY
    # -----------------------------
    entropy = 0
    if packet.haslayer(Raw):
        payload = bytes(packet[Raw].load)
        entropy = calculate_entropy(payload)

    # -----------------------------
    # FEATURES (MATCH TRAINING)
    # -----------------------------
    features = np.array([[ 
        packets,
        bytes_,
        duration,
        proto,
        length,
        bytes_ / max(1, packets),
        packets / max(1, duration),
        bytes_ / max(1, duration),
        flows[key]["syn"],
        flows[key]["ack"],
        entropy
    ]])

    # ✅ SCALE FEATURES
    features_scaled = scaler.transform(features)

    # -----------------------------
    # ML PREDICTION
    # -----------------------------
    proba = model.predict_proba(features_scaled)
    attack_prob = proba[0][1]
    risk_score = int(attack_prob * 100)

    # -----------------------------
    # RULE BOOSTING
    # -----------------------------
    packet_rate = packets / max(1, duration)

    if packet_rate > 50:
        risk_score = max(risk_score, 90)
    elif packet_rate > 20:
        risk_score = max(risk_score, 70)
    elif packet_rate > 10:
        risk_score = max(risk_score, 50)

    if flows[key]["syn"] > flows[key]["ack"] * 2:
        risk_score = max(risk_score, 85)

    if entropy > 6:
        risk_score = max(risk_score, 75)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    if risk_score > 80:
        print(f"🚨 HIGH RISK ({risk_score}%) {src} → {dst} | packets={packets}")
    elif risk_score > 50:
        print(f"⚠️ MEDIUM RISK ({risk_score}%) {src} → {dst} | packets={packets}")
    else:
        print(f"✅ LOW RISK ({risk_score}%) {src} → {dst} | packets={packets}")


# -----------------------------
# START SNIFFING
# -----------------------------
def start_sniffing(model, scaler):
    print("🚀 Starting Advanced IDS Sniffing...\n")

    sniff(
        prn=lambda pkt: process_packet(pkt, model, scaler),
        store=False,
        count=300   # auto stop
    )