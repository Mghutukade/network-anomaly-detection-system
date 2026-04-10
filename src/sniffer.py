from scapy.all import sniff 

def process_packet(packet):
    print(packet.summary())
    
def start_sniffing():
    print("Starting Packet Sniffing")
    sniff(prn=process_packet, count=10)
    