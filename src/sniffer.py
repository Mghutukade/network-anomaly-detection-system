from scapy.all import sniff, IP, TCP, UDP
import numpy as np
import time
from collections import defaultdict

# -------- GLOBAL FLOW STORAGE --------
flows = defaultdict(lambda: {
    "count": 0,
    "bytes": 0,
    "start": time.time(),
    "last_seen": time.time()
})

# -------- PACKET PROCESSING --------
def process_packet(packet, model):
    if not packet.haslayer(IP):
        return

    src = packet[IP].src
    dst = packet[IP].dst
    proto = packet[IP].proto
    key = (src, dst)

    length = len(packet)
    now = time.time()

    # -------- FLOW UPDATE --------
    flow = flows[key]
    flow["count"] += 1
    flow["bytes"] += length
    flow["last_seen"] = now

    duration = now - flow["start"]
    packets = flow["count"]
    bytes_ = flow["bytes"]

    # -------- FEATURE ENGINEERING --------
    features = np.zeros((1, 78))

    # Basic features
    features[0][0] = packets
    features[0][1] = bytes_
    features[0][2] = duration
    features[0][3] = proto
    features[0][4] = length

    # Derived features
    features[0][5] = bytes_ / max(1, packets)        # avg packet size
    features[0][6] = packets / max(1, duration)      # packet rate
    features[0][7] = bytes_ / max(1, duration)       # byte rate

    # TCP features
    if packet.haslayer(TCP):
        flags = int(packet[TCP].flags)
        features[0][8] = flags
        features[0][9] = packet[TCP].sport
        features[0][10] = packet[TCP].dport

    # UDP features
    if packet.haslayer(UDP):
        features[0][11] = packet[UDP].sport
        features[0][12] = packet[UDP].dport

    # -------- ML PREDICTION --------
    try:
        proba = model.predict_proba(features)
        attack_prob = proba[0][1]
        risk_score = int(attack_prob * 100)
    except:
        risk_score = 0  # fallback if model fails

    # -------- RULE-BASED DETECTION --------

    # 🚨 DDoS / Flood detection
    if packets > 100 and duration < 5:
        risk_score = max(risk_score, 95)

    elif packets > 50 and duration < 10:
        risk_score = max(risk_score, 80)

    elif packets > 20:
        risk_score = max(risk_score, 60)

    # 🚨 Ping Flood (ICMP)
    if proto == 1 and packets > 20:
        risk_score = max(risk_score, 85)

    # 🚨 Port scanning (many small packets)
    if packets > 30 and length < 100:
        risk_score = max(risk_score, 75)

    # -------- OUTPUT --------
    if risk_score >= 90:
        print(f"🚨 HIGH RISK ({risk_score}%) {src} → {dst} | packets={packets}")

    elif risk_score >= 60:
        print(f"⚠️ MEDIUM RISK ({risk_score}%) {src} → {dst} | packets={packets}")

    else:
        print(f"✅ LOW RISK ({risk_score}%) {src} → {dst} | packets={packets}")


# -------- START SNIFFING --------
def start_sniffing(model):
    print("🚀 Starting Advanced IDS Sniffing...\n")

    sniff(
        prn=lambda pkt: process_packet(pkt, model),
        store=0,
        count=200  # increase for continuous monitoring
    )