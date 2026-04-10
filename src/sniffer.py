from scapy.all import sniff, IP
import numpy as np

def process_packet(packet, model):
    if packet.haslayer(IP):
        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto
        length = len(packet)

        # -------- FAKE FEATURE VECTOR (78 features) --------
        features = np.zeros((1, 78))  # match model input size
        
        # Fill some meaningful values
        features[0][0] = length
        features[0][1] = proto
        features[0][2] = 1  # dummy packet count

        # Predict
        prediction = model.predict(features)

        if prediction[0] == 1:
            print(f"🚨 ATTACK DETECTED from {src} → {dst}")
        else:
            print(f"✅ Normal traffic: {src} → {dst}")

def start_sniffing(model):
    print("Starting Packet Sniffing")
    
    sniff(
        prn=lambda pkt: process_packet(pkt, model),
        count=50
    )