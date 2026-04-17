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

        # -------- FEATURE VECTOR (78 features) --------
        features = np.zeros((1, 78))

        # Fill important features
        features[0][0] = flows[key]["count"]      # packet count
        features[0][1] = flows[key]["bytes"]      # total bytes
        features[0][2] = duration                 # flow duration
        features[0][3] = proto                    # protocol
        features[0][4] = length                   # packet size

        # -------- PREDICTION --------
        proba = model.predict_proba(features)
        attack_prob = proba[0][1]
        risk_score = int(attack_prob * 100)

        # -------- OUTPUT --------
        if risk_score > 70:
            print(f"🚨 HIGH RISK ({risk_score}%) {src} → {dst} | packets={flows[key]['count']}")
        elif risk_score > 40:
            print(f"⚠️ MEDIUM RISK ({risk_score}%) {src} → {dst} | packets={flows[key]['count']}")
        else:
            print(f"✅ LOW RISK ({risk_score}%) {src} → {dst} | packets={flows[key]['count']}")

def start_sniffing(model):
    print("Starting Packet Sniffing")

    sniff(
        prn=lambda pkt: process_packet(pkt, model),
        count=100
    )