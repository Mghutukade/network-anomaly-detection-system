from flask import Flask
from flask_socketio import SocketIO
import time
import threading
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_simulated_ip():
    return f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def background_sniffer():
    print("🚀 NADS TACTICAL BACKEND ONLINE...")
    protocols = ["TCP", "UDP", "ICMP", "HTTPS"]
    
    while True:
        # 1. Simulate/Get Analysis
        is_anomaly = random.random() > 0.98 # 2% chance of random anomaly
        status = "ANOMALY" if is_anomaly else "NORMAL"
        threat_level = random.randint(85, 99) if is_anomaly else random.randint(0, 4)
        
        # 2. Package the "Intel"
        packet_data = {
            'status': status,
            'threat_level': threat_level,
            'src_ip': get_simulated_ip(),
            'dst_ip': "192.168.1.45", # Your local machine
            'protocol': random.choice(protocols),
            'size': random.randint(40, 1500)
        }
        
        # 3. Emit to Frontend
        socketio.emit('packet', packet_data)
        
        # Fast updates for that "scrolling" feel
        time.sleep(0.8)

if __name__ == '__main__':
    threading.Thread(target=background_sniffer, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)