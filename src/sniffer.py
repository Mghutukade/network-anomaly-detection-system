from scapy.all import sniff, IP, TCP, Raw
import time
import math

from src.predict import hybrid_score, get_label
from src.soc_engine import evaluate_soc
from src.logger import log_event

flows = {}

# ✅ Trusted IPs (Google, Cloudflare, Local)
TRUSTED_IPS = [
    "192.168.",     # local network
    "142.250.",     # Google
    "172.217.",     # Google
    "104.18.",      # Cloudflare
    "172.64."       # Cloudflare
]

# -----------------------------
# ENTROPY
# -----------------------------
def entropy(data):
    if not data:
        return 0
    prob = [data.count(x)/len(data) for x in set(data)]
    return -sum(p * math.log2(p) for p in prob)

# -----------------------------
# PROCESS PACKET
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

    # -----------------------------
    # FLOW INIT
    # -----------------------------
    if key not in flows:
        flows[key] = {
            "packets": 0,
            "bytes": 0,
            "start": now,
            "syn": 0,
            "ack": 0
        }

    f = flows[key]

    f["packets"] += 1
    f["bytes"] += length

    duration = max(1, now - f["start"])

    # -----------------------------
    # TCP FLAGS
    # -----------------------------
    syn = ack = 0
    if packet.haslayer(TCP):
        flags = packet[TCP].flags
        if flags & 0x02:
            syn = 1
        if flags & 0x10:
            ack = 1

    f["syn"] += syn
    f["ack"] += ack

    # -----------------------------
    # ENTROPY
    # -----------------------------
    ent = 0
    if packet.haslayer(Raw):
        ent = entropy(bytes(packet[Raw].load))

    # -----------------------------
    # FEATURES
    # -----------------------------
    features = [
        f["packets"],
        f["bytes"],
        duration,
        proto,
        f["syn"],
        f["ack"],
        ent
    ]

    # -----------------------------
    # 🤖 AI HYBRID SCORE
    # -----------------------------
    score = hybrid_score(features)

    # -----------------------------
    # 🧠 RULE BOOSTING
    # -----------------------------
    packet_rate = f["packets"] / duration

    if packet_rate > 50:
        score = max(score, 90)
    elif packet_rate > 20:
        score = max(score, 70)

    if f["syn"] > f["ack"] * 2:
        score = max(score, 85)

    if ent > 6:
        score = max(score, 75)

    # -----------------------------
    # 🛡️ TRUSTED IP LOGIC (FIXED)
    # -----------------------------
    if any(dst.startswith(ip) for ip in TRUSTED_IPS):
        score = min(score, 40)   # 🔥 not too low (important fix)

    # -----------------------------
    # SOC ENGINE
    # -----------------------------
    soc_event = evaluate_soc(src, dst, score)

    print(f"[{soc_event['severity']}] {score}% | {src} → {dst}")

    log_event({
        "src": src,
        "dst": dst,
        "score": score,
        "severity": soc_event["severity"],
        "time": soc_event["time"]
    })

# -----------------------------
# START
# -----------------------------
def start():
    print("🚨 SOC AI Monitoring Started...")
    sniff(prn=process_packet, store=0)