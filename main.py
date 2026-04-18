from scapy.all import sniff
from src.predict import predict_traffic, get_risk_label


def process_packet(packet):
    try:
        print("\n📡 Packet Captured:")
        print(packet.summary())

        # Example feature extraction (customize later)
        packet_length = len(packet)
        protocol = 6 if packet.haslayer("TCP") else 17
        src_port = packet.sport if hasattr(packet, "sport") else 0
        dst_port = packet.dport if hasattr(packet, "dport") else 0
        flags = 1 if packet.haslayer("TCP") else 0

        features = [packet_length, protocol, src_port, dst_port, flags]

        pred = predict_traffic(features)
        result = get_risk_label(pred)

        print(f"🚨 Prediction: {result}")

    except Exception as e:
        print("Error:", e)


def start():
    print("🚀 Starting Network Monitoring...\n")
    sniff(prn=process_packet, count=10)


if __name__ == "__main__":
    start()