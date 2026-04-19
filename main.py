from src.sniffer import start

# Inside your main.py
def sniff_packet():
    """
    This function bridges your existing AI logic to the Dashboard.
    """
    # 1. Insert your existing Scapy sniffing / Feature extraction logic here
    # 2. Insert your rf_model.predict logic here
    
    # 3. RETURN this exact format so app.py can read it:
    return {
        'ip': "192.168.1.1",      # Replace with actual detected IP
        'size': 512,               # Replace with actual packet size
        'threat': 92,              # Replace with your Model's % prediction
        'entropy': 5.4,            # Replace with calculated entropy or 0
        'flags': "SYN|ACK"         # Replace with actual TCP flags
    }

if __name__ == "__main__":
    start()