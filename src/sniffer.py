from scapy.all import sniff, IP, TCP, Raw
import time
import math

from src.predict import predict_traffic, get_risk_label

flows = {}

def calculate_entropy(data):
    if not data:
        return 0
    prob = [data.count(x)/len(data) for x in set(data)]
    return -sum(p * math.log2(p) for p in prob)


def process_packet(packet):

    if not packet.haslayer(IP):
        return

    src = packet[IP].src
    dst = packet[IP].dst
    proto = packet[IP].proto
    length = len(packet)
    now = time.time()

    key = (src, dst)

    # -----------------------------
    # INIT FLOW
    # -----------------------------
    if key not in flows:
        flows[key] = {
            "packets": 0,
            "bytes": 0,
            "start": now,
            "syn": 0,
            "ack": 0
        }

    flow = flows[key]
    flow["packets"] += 1
    flow["bytes"] += length

    duration = max(1, now - flow["start"])

    # -----------------------------
    # TCP FLAGS
    # -----------------------------
    syn = 0
    ack = 0

    if packet.haslayer(TCP):
        flags = packet[TCP].flags
        if flags & 0x02:
            syn = 1
        if flags & 0x10:
            ack = 1

    flow["syn"] += syn
    flow["ack"] += ack

    # -----------------------------
    # ENTROPY
    # -----------------------------
    entropy = 0
    if packet.haslayer(Raw):
        entropy = calculate_entropy(bytes(packet[Raw].load))

    # -----------------------------
    # FEATURES FOR ML
    # -----------------------------
    features = [
        flow["packets"],
        flow["bytes"],
        duration,
        proto,
        flow["syn"],
        flow["ack"],
        entropy
    ]

    # -----------------------------
    # ML PREDICTION
    # -----------------------------
    ml_prob = predict_traffic(features)

    # -----------------------------
    # RULE ENGINE
    # -----------------------------
    packet_rate = flow["packets"] / duration

    rule_score = 0

    if packet_rate > 50:
        rule_score = 0.9
    elif packet_rate > 20:
        rule_score = 0.7
    elif flow["syn"] > flow["ack"] * 3:
        rule_score = 0.85
    elif entropy > 6:
        rule_score = 0.8

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    final_score = (ml_prob * 0.4) + (rule_score * 0.6)

    label = get_risk_label(final_score)

    print(f"{label} | {src} → {dst}")