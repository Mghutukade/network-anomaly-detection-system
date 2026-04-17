from scapy.all import sniff, IP
import numpy as np
import time

# Store flows
flows = {}

def process_packet(packet, model):
    if packet.haslayer(IP):

        src = packet[IP].src
        dst = packet[IP].dst
        key = (src, dst)

        length = len(packet)
        proto = packet[IP].proto
        now = time.time()

        # -------- FLOW TRACKING --------
        if key not in flows:
            flows[key] = {
                "count": 0,
                "bytes": 0,
                "start": now
            }

        flows[key]["count"] += 1
        flows[key]["bytes"] += length

        duration = now - flows[key]["start"]

        packets = flows[key]["count"]
        bytes_ = flows[key]["bytes"]

        # -------- FEATURE VECTOR --------
        features = np.zeros((1, 78))

        features[0][0] = packets
        features[0][1] = bytes_
        features[0][2] = duration
        features[0][3] = proto
        features[0][4] = length

        # 🔥 EXTRA FEATURES
        features[0][5] = bytes_ / max(1, packets)      # avg packet size
        features[0][6] = packets / max(1, duration)    # packet rate
        features[0][7] = bytes_ / max(1, duration)     # byte rate

        # -------- ML PREDICTION --------
        proba = model.predict_proba(features)
        attack_prob = proba[0][1]
        risk_score = int(attack_prob * 100)

        # -------- SMART DETECTION --------
        if packets > 100:
            risk_score = max(risk_score, 90)
        elif packets > 50:
            risk_score = max(risk_score, 75)
        elif packets > 20:
            risk_score = max(risk_score, 50)

        # -------- OUTPUT --------
        if risk_score > 70:
            print(f"🚨 HIGH RISK ({risk_score}%) {src} → {dst} | packets={packets}")
        elif risk_score > 40:
            print(f"⚠️ MEDIUM RISK ({risk_score}%) {src} → {dst} | packets={packets}")
        else:
            print(f"✅ LOW RISK ({risk_score}%) {src} → {dst} | packets={packets}")


def start_sniffing(model):
    print("Starting Packet Sniffing")

    sniff(
        prn=lambda pkt: process_packet(pkt, model),
        count=100
    )