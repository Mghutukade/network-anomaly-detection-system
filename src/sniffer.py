from scapy.all import sniff, IP, TCP, Raw
import time
import math
import pandas as pd

from src.predict import hybrid_score
from src.soc_engine import evaluate_soc
from src.logger import log_event

flows = {}

# -----------------------------
# TRUSTED IP LIST
# -----------------------------
TRUSTED_IPS = [
    "192.168.",

    # Google
    "142.250.", "172.217.", "192.178.", "142.251.",

    # Cloudflare
    "104.18.", "172.64.",

    # Microsoft / Azure
    "13.", "20.", "40.", "52.",

    # AWS
    "3.", "18.",

    # Local network
    "224.", "239."
]

# -----------------------------
# FEATURE NAMES (IMPORTANT FIX)
# -----------------------------
FEATURE_COLUMNS = [
    "packets",
    "bytes",
    "duration",
    "proto",
    "syn",
    "ack",
    "entropy"
]

# -----------------------------
# ENTROPY FUNCTION
# -----------------------------
def entropy(data):
    if not data:
        return 0
    prob = [data.count(x)/len(data) for x in set(data)]
    return -sum(p * math.log2(p) for p in prob)

# -----------------------------
# MAIN PACKET PROCESSOR
# -----------------------------
def process_packet(packet):

    if not packet.haslayer(IP):
        return

    src = packet[IP].src
    dst = packet[IP].dst
    proto = packet[IP].proto
    length = len(packet)
    now = time.time()

    key = (src, dst)

    if key not in flows:
        flows[key] = {
            "packets": 0,
            "bytes": 0,
            "start": now,
            "syn": 0,
            "ack": 0,
            "last_score": 0
        }

    f = flows[key]

    f["packets"] += 1
    f["bytes"] += length

    duration = max(1, now - f["start"])

    syn = ack = 0

    if packet.haslayer(TCP):
        flags = packet[TCP].flags
        if flags & 0x02:
            syn = 1
        if flags & 0x10:
            ack = 1

    f["syn"] += syn
    f["ack"] += ack

    ent = 0
    if packet.haslayer(Raw):
        ent = entropy(bytes(packet[Raw].load))

    # -----------------------------
    # CREATE DATAFRAME (FIX WARNING)
    # -----------------------------
    features = pd.DataFrame([[
        f["packets"],
        f["bytes"],
        duration,
        proto,
        f["syn"],
        f["ack"],
        ent
    ]], columns=FEATURE_COLUMNS)

    # -----------------------------
    # AI SCORE
    # -----------------------------
    score = hybrid_score(features)

    # -----------------------------
    # RULE BOOSTING (SOC LOGIC)
    # -----------------------------
    packet_rate = f["packets"] / duration

    if packet_rate > 100:
        score = max(score, 90)
    elif packet_rate > 50:
        score = max(score, 75)

    if f["syn"] > f["ack"] * 2:
        score = max(score, 85)

    if ent > 6:
        score = max(score, 75)

    # -----------------------------
    # 🔥 TRUSTED IP STRONG CONTROL
    # -----------------------------
    if any(dst.startswith(ip) for ip in TRUSTED_IPS):
        score = score * 0.4
        score = min(score, 30)

    # -----------------------------
    # SMOOTHING (ANTI-NOISE)
    # -----------------------------
    score = int((score + f["last_score"]) / 2)
    f["last_score"] = score

    # -----------------------------
    # SOC ENGINE
    # -----------------------------
    soc = evaluate_soc(src, dst, score)

    print(f"[{soc['severity']}] {score}% | {src} → {dst}")

    log_event({
        "src": src,
        "dst": dst,
        "score": score,
        "severity": soc["severity"],
        "time": soc["time"]
    })
    
    # If both src & dst are trusted → force LOW
    if any(src.startswith(ip) for ip in TRUSTED_IPS) and any(dst.startswith(ip) for ip in TRUSTED_IPS):
        score = min(score, 25)

# -----------------------------
# START SNIFFER
# -----------------------------
def start():
    print("🚨 SOC AI Monitoring Started...")
    sniff(prn=process_packet, store=0)