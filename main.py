from src.sniffer import process_packet
from scapy.all import sniff

print("🚀 Network IDS Started...")

sniff(prn=process_packet, store=0)